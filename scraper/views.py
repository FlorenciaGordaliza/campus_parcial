from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
import requests
from bs4 import BeautifulSoup

class KeywordForm(forms.Form):
    keyword = forms.CharField(label='Palabra clave', max_length=100)

def hacer_scrap(keyword):
    url = f'https://es.wikipedia.org/w/index.php?search={keyword}'
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = []
    for item in soup.select('.mw-search-result-heading a')[:10]:
        title = item.get_text(strip=True)
        href = 'https://es.wikipedia.org' + item.get('href', '')
        results.append({'titulo': title, 'url': href})
    return results

@login_required
def scraper_view(request):
    results = None
    form = KeywordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        keyword = form.cleaned_data['keyword']
        results = hacer_scrap(keyword)
        lines = [f"{r['titulo']} - {r['url']}" for r in results]
        body = "Resultados del scrap:\n\n" + "\n".join(lines)
        EmailMessage(
            subject=f'Resultados scraper: {keyword}',
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[request.user.email],
        ).send(fail_silently=False)
    return render(request, 'scraper/index.html', {'form': form, 'results': results})