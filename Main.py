import tkinter.filedialog
import shutil
import ocrmypdf
import pdfplumber
import os
import sys
import re
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

#os.chdir(sys._MEIPASS)
data_path = os.path.join('tess_data','por.traineddata')
home_path = os.getcwd()

def cria_diretorio(pasta_ocr):
    try:
        ocr_path = os.mkdir(os.path.join(home_path, pasta_ocr))
        return ocr_path
    except FileExistsError:
        pass

def create_ocr():
    print('work in progress')
    pdf_a_tratar = tkinter.filedialog.askopenfilename()

    diretorio_ocr = cria_diretorio('OCR-CRIADOS')
    pdf_alvo = shutil.copy2(pdf_a_tratar, home_path)
    pdf_alvo_name = os.path.basename(pdf_alvo).replace(" ","")

    i = ""
    for s in pdf_alvo_name:
        i=i+s
    pdf_fim = str(i)

    pdf_alvo = os.rename(pdf_alvo, pdf_alvo_name)

    texto_tkinter.set("Seu arquivo será renomeado \npara "+pdf_alvo_name+ ".Aguarde" )

    if __name__ == '__main__':
        os.system('ocrmypdf -l eng+por --deskew --rotate-pages --skip-text' +' '+i + " "+ i)

        shutil.move(pdf_alvo_name, os.path.join(home_path,'OCR-CRIADOS'))
        texto_tkinter.set("Conversão concluída Enviando para a pasta OCR-CRIADOS")

        #def texto_ocr(): #teste com ocrmypdf. para remover arquivo txt basta recomer a flag --sidecar output.txt
        #os.system('ocrmypdf -l eng+por --deskew --rotate-pages --remove-background --sidecar vr.csv VR.pdf VR-OCR.pdf')

def cria_lista_ocr():

    texto_tkinter.set('Iniciando a conversao. Aguarde')
    print('work in progress')

    tuplaDocs = tkinter.filedialog.askopenfilenames(title='selecione os pdfs a serem convertidos',
                                                  filetypes=[("pdf", ".pdf")])

    diretorio_ocr = cria_diretorio('OCR-CRIADOS')

    for pdf in tuplaDocs:
        # print(os.path.basename(pdf))
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

            #ocrmypdf.ocr('original','original.pdf', deskew=True, skip_text=True, rotate_pages=True)

            pdf_alvo = i
            shutil.move(pdf_alvo_name, os.path.join(home_path,'OCR-CRIADOS'))
            texto_tkinter.set(f'Conversão concluída\n Enviando {pdf_alvo_name}para a pasta OCR-CRIADOS')


# def recorta_paginas_pesquisadas(): # base no Pypdf2
#     path_to_pdf = extract_whole()
#     with open(path_to_pdf, 'rb') as file:
#         reader = PyPDF2.PdfFileReader(file)
#         pdfWriter = PyPDF2.PdfFileWriter()
#         pages = impressao
#
#         if len(impressao) > 0:
#
#             for page in pages:
#                 pdfWriter.addPage(reader.getPage(page))
#
#             with open ('{0}_extraido.pdf'.format(path_to_pdf), 'wb') as f:
#                 pdfWriter.write(f)
#                 f.close()
#
#             texto_tkinter.set("Separação concluída")
#
#         else:
#             texto_tkinter.set('não há páginas a serem impressas')
#     impressao.clear()


def merger(): # funciona bem
    file_names = tkinter.filedialog.askopenfilenames()
    mergerpdf = PyPDF2.PdfFileMerger()

    for pdf in file_names:
        with open(pdf, "rb") as file:
            mergerpdf.append(pdf)

    with open("merger.pdf", "wb") as f:
        mergerpdf.write(f)

    texto_tkinter.set("Work in progress")

def renameallSeiDocs():
    # Funcionou. Vai remover todos os pdfs da pasta e renomeá-los
    seiDocs = tkinter.filedialog.askopenfilenames(title='selecione os pdfs a serem renomeados',
                                                                  filetypes=[("pdf",".pdf")])

    for pdf in seiDocs:
        # print(os.path.basename(pdf))
        cortado = pdf.split("-")
        os.rename(pdf, cortado[1])

def meta_data():

    pdf = pdfplumber.open(str(tkinter.filedialog.askopenfilename()))

    print("Number of pages : {}".format(len(pdf.pages)))
    print("Pages : {}".format(pdf.pages))

    print("Document Information")
    print(pdf.metadata)

    print("Author name : {}".format(pdf.metadata["Author"]))
    print("Creator : {}".format(pdf.metadata["Creator"]))

    pdf.close()

# def extract_whole(): # com pdfplumber. Funciona melhor
#     documento = tkinter.filedialog.askopenfilename()
#     pdf = pdfplumber.open(documento)
#     n = len(pdf.pages)
#     nome_a_extrair = str(input_nome.get().lower())
#     print(nome_a_extrair)
#     regex = re.compile(nome_a_extrair, flags=re.I)
#
#     try:
#
#         for page in range(n):
#
#         # for page in pdf.pages:
#             data = pdf.pages[page].extract_text().lower()
#             print(data)
#             # if regex.search(data):
#             #     impressao.append(page)
#
#             if nome_a_extrair in data:
#                 impressao.append(page)
#
#         print(impressao)
#         texto_tkinter.set('nome encontrado em '+ str(impressao[-1])+ ' páginas.\n Extraindo...')
#         input_nome.delete(0,END)
#
#     except:
#         pdf.close()
#         texto_tkinter.set('Erro. Nome não encontrado \n Tente novamente')
#         input_nome.delete(0,END)
#
#         return
#
#     pdf.close()
#     return  documento


# usando tkinter (modularizar dp)

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


btn_renameSeiDocs = Button(frame1, text="RENOMAER DOCS SEI", command=renameallSeiDocs,
                        width=60, height=1, anchor=CENTER, fg=branco, bg=verde)
btn_renameSeiDocs.grid(row=3,column=0, sticky=NSEW, pady=1)

# btn_converter_pdf_para_ocr = Button(frame1, text="CONVERTER UM PDF EM FORMATO PESQUISAVEL", command=create_ocr,
#                                     width=60, height=1, anchor=CENTER, bg=vermelho, fg=branco)

btn_converter_pdf_para_ocr = Button(frame1, text="CONVERTER UM PDF EM FORMATO PESQUISAVEL", command=cria_lista_ocr,
                                    width=60, height=1, anchor=CENTER, bg=vermelho, fg=branco)
btn_converter_pdf_para_ocr.grid(row=4,column=0, sticky=NSEW, pady=1)

btn_extrair_pagina_nome = Button(frame1, text="JUNTAR PDF", command=merger,
                                 width=60, height=1, anchor=CENTER, bg=azul, fg=branco)
btn_extrair_pagina_nome.grid(row=5,column=0, sticky=NSEW, pady=1)

# input_nome = Entry(frame1, width=60)
# input_nome.grid(row=6,column=0, sticky=NSEW, pady=1)

# label_pesquisar = Label(frame1, text="Para separar as páginas com base em um nome,\n digite acima o nome a ser pesquisado e depios\n CLIQUE no botão",
#                          width=20, height=5, anchor=CENTER, fg=vermelho)
# label_pesquisar.grid(row=7,column=0,sticky=NSEW, pady=1)


#Informações de LOG
texto_tkinter = StringVar()
texto_tkinter.set("")
label_log = Label(frame1, textvariable=texto_tkinter,
                         width=20, height=2, anchor=CENTER)
label_log.grid(row=8,column=0,sticky=NSEW, pady=1)

janela.mainloop()