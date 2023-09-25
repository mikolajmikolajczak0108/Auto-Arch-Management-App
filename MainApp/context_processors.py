from .forms import MessageForm
from .models import Messages, Users

def message_form(request):
    if request.user.is_authenticated:
        messages = Messages.objects.filter(receiver_id=request.user.user_id).prefetch_related('attachments')
        users = Users.objects.all()
        return {'form': MessageForm(), 'messages': messages, 'users': users}
    else:
        return {}
