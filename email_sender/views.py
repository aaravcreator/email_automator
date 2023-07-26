
from django.shortcuts import render,HttpResponse,redirect
from.utils import send_mail_to_user
from .forms import *
import csv
import re
from django.core.mail import EmailMessage
def index(request):
    return render(request,'home.html')

def send_mail(request):
    message = request.GET.get('message')
    print(message)
    if message is not None:
        send_mail_to_user(['m.sujanpaudel256@gmail.com'],'Mail from Django',"THis is mail from django app and message is {}".format(message))
        print('message sent -  {}'.format(message))
        return HttpResponse("Mail sent to m.sujanpaudel256@gmail.com ")
    return render(request,'home.html')



def send_single_mail(request):
    form = SingleEmailForm()
    if request.method == 'POST':
        form = SingleEmailForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            body = form.cleaned_data.get('message')

            from_email = 'poudelaarav@gmail.com'  # Replace with your email address
            email_message = EmailMessage(subject, body,from_email, [email])
            email_message.send()
         
            # return render(request,'single_mail.html',{ 'form':form,'message_list':body})
            return redirect('send_single_mail')
    return render(request,'single_mail.html',{'form':form})


def send_bulk_mail(request):
    form = EmailTemplateForm()
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST,request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            csv_file = form.cleaned_data['file']
            # csv_file = request.FILES['csv_file']
        
            reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
            next(reader)  # Skip the header row if it exists
            
            messages = []
            template = form.cleaned_data.get('message_template')
            subject = form.cleaned_data.get('subject')
            only_gen = form.cleaned_data.get('only_gen')
            for row in reader:
                if len(row)>=4:
                    email = row[0]
                    col1= row[1]
                    col2 = row[2]
                    col3 = row[3]
                else:
                    email = row[0]
                    col1= row[1]
                    col2 = row[2]
                    col3 = ""

                
                # Template message
                # Fill in the template with actual values
                dynamic_message = re.sub(r'\{col1\}', col1, template)
                dynamic_message = re.sub(r'\{col2\}', col2, dynamic_message)
                dynamic_message = re.sub(r'\{col3\}',col3,dynamic_message)
                
                messages.append(dynamic_message)


                subject = subject
                body = dynamic_message
                from_email = 'poudelaarav@gmail.com'  # Replace with your email address
                
                email_message = EmailMessage(subject, body, from_email, [email])
                if not only_gen:
                    email_message.send()
            # Join all the messages with a line break
            final_message = '\n'.join(messages)
            print(final_message)
            # Return the final message as a response
            # return 
            return render(request,'email_template.html',{'form':form,'message_list':messages,'only_gen':only_gen})

    return render(request,'email_template.html',{'form':form})