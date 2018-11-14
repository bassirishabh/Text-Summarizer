import os
from wsgiref.util import FileWrapper
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
import PyPDF2
from django.shortcuts import render, HttpResponse, redirect
from django.utils.encoding import smart_str
from django.views import View

from .forms import getFileModel, RegistrationForm, LoginForm, urlform, demoform
from .models import getFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


def home(request):
    return render(request, 'index.html')


def logoutt(request):
    logout(request)
    return render(request, 'index.html', {})


def sendimage(receiver, dirname, path):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email import encoders

    fromaddr = "akshaykumar.90447@gmail.com"
    toaddr = receiver

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Summary"

    body = "download attachment for summary"

    msg.attach(MIMEText(body, 'plain'))

    filename = "summary.txt"
    path_name = os.path.join(path, dirname)
    path_final = os.path.join(path_name, filename)
    print(path_final)
    attachment = open(path_final, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "piplani@786")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def form(request):
    if request.method == 'POST':
        form = getFileModel(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            obj = getFile()  # gets new object
            obj.user = str(request.user.username)
            print(obj.user)
            obj.file = form.cleaned_data['file']
            obj.length = form.cleaned_data['length']
            print(request.user.email)
            # finally save the object in db
            obj.save()
            print("id", obj.id)
            dire = str(obj.id)
            path = settings.MEDIA_ROOT
            old_path = path + '/' + str(obj.file.name)
            new_path = path + '/' + dire
            os.mkdir(new_path)
            new_path = new_path + '/' + str(obj.file.name)
            os.rename(old_path, new_path)
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            path_name = os.path.join(path, filename)
            # fil = open(os.path.join(path,dire+'.txt'),'w')
            # if file.name.endswith('.pdf'):
            #     pdfFileObj = open(os.path.join(os.path.join(path,dire),file.name), 'rb')
            #     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            #     for i in range(pdfReader.numPages):
            #         pageObj = pdfReader.getPage(i)
            #         print(pageObj.extractText())
            #         fil.write(pageObj.extractText()+"\n")
            #         print('pdf')
            #     pdfFileObj.close()
            #     fil.close()
            #     filename = dire+'.txt'
            os.system('python ' + path + '\summary.py ' + str(
                obj.length) + " " + path_name + " " + filename + " " + path + " " + dire)
            sendimage(str(request.user.email), dire, path)
            # f = open(path_name, 'r')
            #   print(l)
            return render(request, 'Summarizer/result.html')
    else:
        form = getFileModel()
    return render(request, 'Summarizer/form.html', {'form': form})


def detail(request):
    all_files = getFile.objects.filter(user=request.user.username)
    path = settings.MEDIA_ROOT
    print(path)
    context = {
        'path': path,
        'files': all_files
    }
    print(all_files)
    return render(request, 'Summarizer/detail.html', context)


def download(reques, file):
    file_name = getFile.objects.get(file=file)
    path = settings.MEDIA_ROOT
    path_name = os.path.join(path, file)
    print(file_name)
    path_to_file = "/media/{0}".format(file_name)
    response = HttpResponse(open(path_name, "rb"), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    response['X-Sendfile'] = smart_str(path_to_file)
    return response


def download1(reques, id):
    file_name = 'summary.txt'
    path = os.path.join(settings.MEDIA_ROOT, str(id))
    path_name = os.path.join(path, file_name)
    # print(file_name)
    print(path_name)
    path_to_file = "/media/{0}".format(file_name)
    response = HttpResponse(open(path_name, "rb"), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    response['X-Sendfile'] = smart_str(path_to_file)
    return response


def register(request):
    passw = False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Summarizer/login/')
        else:
            passw = True
            args = {'form': form, 'passw':passw}
            return render(request, 'Summarizer/register.html', args)
            # return redirect('/Summarizer/error')
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'Summarizer/register.html', args)


class LoginUserform(View):
    Form = LoginForm
    template = 'Summarizer/login.html'

    def get(self, request):
        form = self.Form(None)

        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, self.template, {'form': form, 'error': 'User has been Deactivated'})

            else:
                return render(request, self.template, {'form': form, 'error': 'Username and Password does not match'})

        else:
            return render(request, self.template, {'form': form, 'error': 'Enter the form correctly'})


def messagesend(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        message = message + " " + "Mobile Number " + phone
        from_email = request.POST.get('email')
        email = EmailMessage("Contact Form", message, from_email, ['logerine388@gmail.com'])
        email.send()

        print(name)
        return render(request, 'Summarizer/contact.html')


def check(request):
    return redirect("http://gmail.com/")


def url(request):
    form = urlform(request.POST or None)
    st = ""
    err = False
    f = False
    if form.is_valid():
        cd = form.cleaned_data
        urlname = cd.get('urlname')
        count = cd.get('count')
        print(urlname)
        print(count)

        import sys
        import os
        from sumy.parsers.html import HtmlParser
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lsa import LsaSummarizer as Summarizer
        from sumy.nlp.stemmers import Stemmer
        from sumy.utils import get_stop_words

        LANGUAGE = "english"
        try:

            parser = HtmlParser.from_url(urlname, Tokenizer(LANGUAGE))
            stemmer = Stemmer(LANGUAGE)
            summarizer = Summarizer(stemmer)
            summarizer.stop_words = get_stop_words(LANGUAGE)
            f = True
            for sentence in summarizer(parser.document, count):
                print(sentence)
                st += str(sentence) + "\n"
            st1 = ""
        except:
            err = True
            f = True
        return render(request, 'Summarizer/url.html', {'form': form, 'str': st, 'f': f,'err':err})
    else:
        return render(request, 'Summarizer/url.html', {'form': form, 'str': st, 'f': f,'err':err})


def demo(request):
    f=0
    form = demoform(request.POST or None)
    st = ""
    if form.is_valid():
        f=1
        cd = form.cleaned_data
        text = cd.get('text')
        count = cd.get('count')
        print(text)
        print(count)
        import sys
        import os
        from sumy.parsers.html import HtmlParser
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lsa import LsaSummarizer as Summarizer
        from sumy.nlp.stemmers import Stemmer
        from sumy.utils import get_stop_words
        LANGUAGE = "english"
        print(sys.argv)
        # st = "dhasvfasvvfdkiqhafcb ahksfbasfjabdhkc aksjbfasj"
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        for sentence in summarizer(parser.document, count):
            print(type(sentence))
            print(sentence)
            st += str(sentence) + "\n"

    return render(request, 'Summarizer/demo.html', {'form': form, 'st': st,'f':f})
