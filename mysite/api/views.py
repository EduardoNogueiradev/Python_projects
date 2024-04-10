from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 

# Importa de dentro do arquivo 'forms' a classe para validar o formulário 
from .forms import FileForm

# Importa de dentro da pasta 'untils' o script para comparar as planilhas
from .untils.compare_sheets import compare_sheets


# Rota GET '/' retorna a página inicial 'index.html'
def index(request):
  return render(request, "api/index.html")
    

# Rota POST '/get_sheets' executa e retorna o resultado do script
@csrf_exempt
def get_sheets(request):
  # Verifica o método da requisição
  if request.method == 'POST':
    form = FileForm(request.POST, request.FILES)
    print(form)

    # Verifica se o formulário é válido
    if form.is_valid():
      if form.cleaned_data['columns']:
        columns = form.cleaned_data['columns']
      else:
        columns = []

      # Envia o corpo da solicitação para o script
      output = compare_sheets(request.FILES, columns)
      return HttpResponse(output, status=200)
    else:
      return HttpResponse("not valid", status=400)
  else: 
    return HttpResponse("method is not valid", status=405)
