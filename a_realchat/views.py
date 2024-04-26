from django.shortcuts import render,get_object_or_404,redirect
from .models import GroupChat,GroupMessage
from .form import ChatMessageCreateForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def Home(request):
    chat_group = get_object_or_404(GroupChat,group_name='TalkAboutPython')
    #to get letest 30 messages in group
    chat_message = chat_group.chat_message.all()[:30]
    form = ChatMessageCreateForm()
    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.auther = request.user
            chat.group = chat_group
            chat.save()
            context = {'message':chat,'user':request.user}
            # creating a separate HTML file for rendering chat messages within the "partials" directory enhances code organization, 
            # promotes reusability, and adheres to common conventions in web development.
            return render(request,'a_realchat/partials/chat_message_p.html',context)
        else:
            form = ChatMessageCreateForm()

    context = {"chat_message":chat_message,"form": form}
    return render(request, 'a_realchat/chat.html',context)