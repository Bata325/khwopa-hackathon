from django.shortcuts import render

def upload_video(request):
    # Add logic for uploading video
    return render(request, 'admin/upload_video.html')

def live_video(request):
    # Add logic for displaying live video
    return render(request, 'admin/live_video.html')

def recent_tasks(request):
    # Add logic for displaying recent tasks
    return render(request, 'admin/recent_tasks.html')
