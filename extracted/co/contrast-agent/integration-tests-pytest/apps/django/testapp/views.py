from __future__ import annotations

import os
import subprocess

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .models import Message
import json


def shell_clock(request: HttpRequest):
    format = request.GET.get("format", "+%H:%M:%S")
    time = subprocess.check_output(f"date {format}", shell=True).strip().decode()
    return HttpResponse(
        f"<html><body><h1>Current Time</h1><p>{time}</p></body></html>".encode()
    )


def system_sleep(request: HttpRequest):
    duration = float(request.GET.get("duration", 0.1))
    os.system(f"sleep {duration}")
    return HttpResponse(
        f"<html><body><h1>Slept for {duration} seconds</h1></body></html>".encode()
    )


@method_decorator(csrf_exempt, name="dispatch")
class PostsView(View):
    POSTS_DIR = "posts"

    def get(self, request: HttpRequest, name: str | None = None):
        if name is None:
            # List all posts
            posts = os.listdir(self.POSTS_DIR)
            posts_list = "".join(f"<li>{post}</li>" for post in posts)
            return HttpResponse(
                f"<html><body><h1>Posts</h1><ul>{posts_list}</ul></body></html>".encode()
            )
        else:
            post_path = os.path.join(self.POSTS_DIR, name)
            if not os.path.isfile(post_path):
                return HttpResponse(
                    f"<html><body><h1>Not Found</h1><p>Post '{name}' does not exist.</p></body></html>".encode(),
                    status=404,
                )
            with open(post_path, "rb") as f:
                content = f.read()
            return HttpResponse(content)

    def post(self, request: HttpRequest, name: str):
        post_path = os.path.join(self.POSTS_DIR, name)
        with open(post_path, "wb") as f:
            f.write(request.body)
        return HttpResponse(
            f"<html><body><h1>Post '{name}' saved.</h1></body></html>".encode()
        )


# Prep the filesystem for PostsView
os.makedirs(PostsView.POSTS_DIR, exist_ok=True)
example_post_path = os.path.join(PostsView.POSTS_DIR, "example.txt")
with open(example_post_path, "w") as f:
    f.write("This is an example post.\n")


@csrf_exempt
def messages_view(request: HttpRequest):
    """
    GET: List all messages as JSON.
    POST: Create a new message with JSON body: {"text": "..."}
    """
    if request.method == "GET":
        messages = Message.objects.order_by("-created_at")
        data = [
            {"id": m.id, "text": m.text, "created_at": m.created_at.isoformat()}
            for m in messages
        ]
        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        try:
            payload = json.loads(request.body.decode())
            text = payload.get("text", "")
            if not text:
                return JsonResponse({"error": "Missing 'text' field"}, status=400)
            msg = Message.objects.create(text=text)
            return JsonResponse(
                {
                    "id": msg.id,
                    "text": msg.text,
                    "created_at": msg.created_at.isoformat(),
                },
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
