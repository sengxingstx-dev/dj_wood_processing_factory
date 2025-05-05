def global_messages(request):
    # You can return a static message or make it dynamic based on request/session
    return {
        "msg": "This is a global message",
        "confirm_msg": "Are you sure you want to log out?",
    }
