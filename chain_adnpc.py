from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
import json
import dotenv

dotenv.load_dotenv()

def chat(file_path_peticao_inicial):
    prompt_template = PromptTemplate.from_template(
        """
        O documento abaixo é uma petição inicial de um processo judicial. Resposta as perguntas apresentadas logo depois do texto.

        <petição inicial>
        {peticao_inicial}
        <\petição inicial>

        Responda no formato de JSON:

        
            "adicional_noturno_PCPA": true/false, # Verifique se o caso se trata de ação ajuizada por policial pertencente aos quadros da Polícia Civil do Estado do Pará, em que alega ter direito ao recebimento do adicional noturno, conforme disposto na legislação vigente, argumentando que a natureza de suas atividades, realizadas em horários noturnos, confere o direito ao referido adicional.          
        

        """
    )

    loader = PyPDFLoader(file_path_peticao_inicial)
    
    arquivo = loader.load()    
       
    texto_peticao_inicial = ''
    
    for page in arquivo:
        texto_peticao_inicial+=page.page_content

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    chain=prompt_template|llm|StrOutputParser()

    #verificar se o arquivo é menor que 51 páginas
    if len(arquivo)<51:
        resposta_chain=chain.invoke({'peticao_inicial': texto_peticao_inicial})    
        
    else: 
        raise ValueError ("Erro: o arquivo da petição inicial não pode ter mais que 50 páginas")

    print(resposta_chain)
    return json.loads(resposta_chain.replace('```json\n','').replace('\n```',''))

if __name__ == "__main__": 
    print(chat('.\Adicional Noturno - PC PA - Petição Inicial (202401019217).pdf'))
