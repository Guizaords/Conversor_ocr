import tkinter.filedialog
import shutil
import ocrmypdf
import pdfkit as pdfkit
import pdfplumber
import os
import sys
import PyPDF2
from tkinter import *

# PALETA DE CORES
preto = "#000000"  # black
vermelho = "#cc1d4e"  # red
branco = "#feffff"  # white
azul = "#0074eb"  # blue
co4 = "#435e5a"  # #435e5a
verde = "#59b356"  # green
cinza = "#d9d9d9"  # grey

impressao = []
data_path = os.path.join('tess_data','por.traineddata')
home_path = os.getcwd()

def cria_diretorio(pasta):
    try:
        ocr_path = os.mkdir(os.path.join(home_path, pasta))
        return ocr_path
    except FileExistsError:
        pass

def cria_lista_ocr():

    texto_tkinter.set('Iniciando a conversao. Aguarde')
    print('work in progress')

    tuplaDocs = tkinter.filedialog.askopenfilenames(title='selecione os pdfs a serem convertidos',
                                                  filetypes=[("pdf", ".pdf")])

    diretorio_ocr = cria_diretorio('OCR-CRIADOS')

    for pdf in tuplaDocs:
        pdf_alvo = shutil.copy2(pdf, home_path)
        pdf_alvo_name = os.path.basename(pdf).replace(" ", "-")

        i = ""
        for s in pdf_alvo_name:
            i=i+s
        pdf_fim = str(i)
        pdf_alvo = os.rename(pdf_alvo, pdf_alvo_name)
        texto_tkinter.set("Seu arquivo será renomeado \npara "+pdf_alvo_name+ ".Aguarde" )
        if __name__ == '__main__':
            os.system('ocrmypdf -l eng+por --deskew --rotate-pages --skip-text' +' '+i + " "+ i)
            pdf_alvo = i
            shutil.move(pdf_alvo_name, os.path.join(home_path,'OCR-CRIADOS'))
            texto_tkinter.set(f'Conversão concluída\n Enviando {pdf_alvo_name}para a pasta OCR-CRIADOS')


def merger(): # funciona bem
    file_names = tkinter.filedialog.askopenfilenames(title='selecione os arquivos PDF a serem unidos',
                                                                  filetypes=[("pdf",".pdf")])
    mergerpdf = PyPDF2.PdfFileMerger()
    diretorio_ocr = cria_diretorio('PDFS UNIDOS')
    texto_tkinter.set("Juntando arquivos... aguarde")
    for pdf in file_names:
        with open(pdf, "rb") as file:
            mergerpdf.append(pdf)
    with open("merger.pdf", "wb") as f:
        mergerpdf.write(f)
    shutil.move('merger.pdf', os.path.join(home_path, 'PDFS UNIDOS'))
    texto_tkinter.set(f'Conversão concluída\n Enviado para a pasta PDFS UNIDOS')

def converte_html_pdf():
    # Funcionou. Vai remover todos os pdfs da pasta e renomeá-los
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    diretorio_html = cria_diretorio('HTML-CONVERTIDOS')
    seiHtmls = tkinter.filedialog.askopenfilenames(title='selecione os arquivos HTML a serem convertidos',
                                                                  filetypes=[("html",".html")])
    texto_tkinter.set("Convertendo arquivos... aguarde")
    for html in seiHtmls:
        html_copy = shutil.copy2(html,home_path)
        pdf = pdfkit.from_file(html_copy, f'{html_copy}.pdf', configuration=config)
        os.remove(html_copy)

    for pdf in os.listdir(home_path):
        if 'pdf' in pdf:
            shutil.move(pdf, os.path.join(home_path,'HTML-CONVERTIDOS'))

    texto_tkinter.set(f'Conversão concluída\n Enviados para a pasta HTML-CONVERTIDOS')

def extrai_e_recorta(): # com pdfplumber. Funciona melhor
    nome_a_extrair = str(input_nome.get().lower())
    if nome_a_extrair == "":
        texto_tkinter.set("nome não pode ser vazio")
        return
    tupla_pdf = tkinter.filedialog.askopenfilenames(title='selecione os arquivos PDF a serem extraidos',
                                                                  filetypes=[("pdf",".pdf")])
    diretorio_extraidos = cria_diretorio('PDF-EXTRAIDOS')


    for _pdf in tupla_pdf:
        documento_pdf = shutil.copy2(_pdf,home_path)

        lista_pages = []
        pdf = pdfplumber.open(documento_pdf)
        reader = PyPDF2.PdfFileReader(documento_pdf)
        pdfWriter = PyPDF2.PdfFileWriter()
        n = len(pdf.pages)
        nome_a_extrair = str(input_nome.get().lower())
        print(nome_a_extrair)

        try:
            for page in range(n):
                data = pdf.pages[page].extract_text().lower()
                if nome_a_extrair in data:
                    lista_pages.append(page)
                    print(lista_pages)

            texto_tkinter.set('nome encontrado em '+ str(lista_pages[-1])+ ' páginas.\n Extraindo...')

            if len(lista_pages) > 0:
                for pagina in lista_pages:
                    pdfWriter.addPage(reader.getPage(pagina))

                    with open('{0}_extraido.pdf'.format(documento_pdf), 'wb') as f:
                        pdfWriter.write(f)

                texto_tkinter.set("Separação concluída")

            else:
                texto_tkinter.set('não há páginas a serem impressas')

        except:
            pdf.close()
            texto_tkinter.set('Erro. Nome não encontrado \n Tente novamente')
            input_nome.delete(0,END)
            return
        lista_pages.clear()
        pdf.close()
    input_nome.delete(0, END)
    for pdf in os.listdir(home_path):
        if 'extraido.pdf' in pdf:
            shutil.move(pdf, os.path.join(home_path,'PDF-EXTRAIDOS'))
        elif '.pdf' in pdf:
            os.remove(pdf)

    texto_tkinter.set(f'Conversão concluída\n Enviados para a pasta PDF-EXTRAIDOS')

# def renameallSeiDocs():
#     # Funcionou. Vai remover todos os pdfs da pasta e renomeá-los
#     seiDocs = tkinter.filedialog.askopenfilenames(title='selecione os pdfs a serem renomeados',
#                                                                   filetypes=[("pdf",".pdf")])
#
#     for pdf in seiDocs:
#         # print(os.path.basename(pdf))
#         cortado = pdf.split("-")
#         os.rename(pdf, cortado[1])
# def meta_data():
#
#     pdf = pdfplumber.open(str(tkinter.filedialog.askopenfilename()))
#
#     print("Number of pages : {}".format(len(pdf.pages)))
#     print("Pages : {}".format(pdf.pages))
#
#     print("Document Information")
#     print(pdf.metadata)
#
#     print("Author name : {}".format(pdf.metadata["Author"]))
#     print("Creator : {}".format(pdf.metadata["Creator"]))
#
#     pdf.close()
janela = Tk()
janela.geometry("400x400")
janela.title("Tratamento de pdf")
#janela.resizable(width=0, height=0)
frame1 = Frame(janela, width=400, height=250, relief="flat")
frame1.grid(row=0,column=0)

#nome do app
app_name = Label(frame1, text="PDF-TREATMENT",
                 width=24, height=1, anchor=CENTER)
app_name.grid(row=0,column=0,sticky=NSEW, pady=1)

#Botão que vai selecionar o arquivo a ser tratado
label_selecionar = Label(frame1, text="O que você gostaria de fazer?",
                         width=24, height=1, anchor=CENTER)
label_selecionar.grid(row=1,column=0,sticky=NSEW, pady=1)

#Botao que converter html para pdf
btn_converter_html_pdf = Button(frame1, text="CONVERTER HTML EM PDF", command=converte_html_pdf,
                        width=60, height=1, anchor=CENTER, fg=branco, bg=verde)
btn_converter_html_pdf.grid(row=3,column=0, sticky=NSEW, pady=1)

# Botao que transforma pdf em pesquisavel

btn_converter_pdf_para_ocr = Button(frame1, text="CONVERTER UM PDF EM FORMATO PESQUISAVEL", command=cria_lista_ocr,
                                    width=60, height=1, anchor=CENTER, bg=vermelho, fg=branco)
btn_converter_pdf_para_ocr.grid(row=4,column=0, sticky=NSEW, pady=1)

# Botao que faz o merge dos pdfs
btn_juntar_pdf = Button(frame1, text="JUNTAR PDF", command=merger,
                                 width=60, height=1, anchor=CENTER, bg=azul, fg=branco)
btn_juntar_pdf.grid(row=5,column=0, sticky=NSEW, pady=1)


# Botao que extrai as páginas
btn_extrair_pagina_nome = Button(frame1, text="SEPARAR PDF COM BASE EM UM NOME", command=extrai_e_recorta,
                                 width=60, height=1, anchor=CENTER, bg=preto, fg=branco)
btn_extrair_pagina_nome.grid(row=7,column=0, sticky=NSEW, pady=1)


input_nome = Entry(frame1, width=60)
input_nome.grid(row=6,column=0, sticky=NSEW, pady=1)

label_pesquisar = Label(frame1, text="Para separar as páginas com base em um nome,\n digite acima o nome a ser pesquisado e depios\n CLIQUE no botão",
                         width=20, height=5, anchor=CENTER, fg=vermelho)
label_pesquisar.grid(row=9,column=0,sticky=NSEW, pady=1)


#Informações de LOG
texto_tkinter = StringVar()
texto_tkinter.set("")
label_log = Label(frame1, textvariable=texto_tkinter,
                         width=20, height=2, anchor=CENTER)
label_log.grid(row=8,column=0,sticky=NSEW, pady=1)

janela.mainloop()