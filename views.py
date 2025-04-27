from django.shortcuts import render
from .utils import extract_text_from_resume, calculate_score
from .utils import match_job_description
from django.http import JsonResponse
from .chatbot import create_chatbot, chat_with_bot
from django.shortcuts import render
from .forms import CandidateForm
from .models import Candidate, Job
from .utils import extract_text_from_resume, rank_resume_by_keywords
from .video_analysis import analyze_facial_expression
import matplotlib.pyplot as plt
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse

def upload_resume(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            text = extract_text_from_resume(candidate.resume.path)

            # Fetch a job (use your logic to select the right job)
            job = Job.objects.first()  # Or implement a matching mechanism

            # Rank the candidate based on the job description
            candidate_score = rank_resume_by_keywords(text, job)
            candidate.score = candidate_score
            candidate.save()

            return render(request, 'success.html', {'candidate': candidate})
    else:
        form = CandidateForm()
    return render(request, 'upload.html', {'form': form})

def upload_resume(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            text = extract_text_from_resume(candidate.resume.path)

            # Fetch job (use appropriate logic to find the job)
            job = Job.objects.first()

            # Match resume to the job description and get similarity score
            similarity_score = match_job_description(text, job)
            candidate.score = similarity_score
            candidate.save()

            return render(request, 'success.html', {'candidate': candidate})
    else:
        form = CandidateForm()
    return render(request, 'upload.html', {'form': form})

def chatbot_interaction(request):
    chatbot = create_chatbot()
    user_input = request.GET.get('user_input')
    if user_input:
        response = chat_with_bot(chatbot, user_input)
        return JsonResponse({"response": str(response)})
    return render(request, 'chatbot.html')

def analyze_video(request, video_file):
    # Process the video file and analyze emotions
    video_path = video_file.path
    emotion_score = analyze_facial_expression(video_path)
    
    return JsonResponse({"emotion_score": emotion_score})


def recruitment_dashboard(request):
    # Example candidate scores data
    data = {
        'Candidates': ['Alice', 'Bob', 'Charlie'],
        'Score': [80, 75, 90],
        'Status': ['Shortlisted', 'Rejected', 'Shortlisted']
    }
    df = pd.DataFrame(data)
    
    # Create a plot
    fig, ax = plt.subplots()
    ax.bar(df['Candidates'], df['Score'])
    ax.set_xlabel('Candidates')
    ax.set_ylabel('Scores')
    ax.set_title('Candidate Scores')

    # Save the plot to an image
    plt.savefig('candidate_scores.png')

    # Return the image in response
    with open('candidate_scores.png', 'rb') as f:
        image_data = f.read()
    
    return HttpResponse(image_data, content_type='image/png')


