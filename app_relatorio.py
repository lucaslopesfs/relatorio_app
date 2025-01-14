import streamlit as st
import pandas as pd

# Função para carregar a planilha
def carregar_planilha():
    uploaded_file = st.file_uploader("Escolha uma planilha Excel", type=["xlsx", "xls"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        return df
    return None

# Função para criar o relatório com base no texto
def gerar_relatorio(df, texto_base):
    # Substituir tags no texto base pelas colunas correspondentes
    for coluna in df.columns:
        tag = f"[{coluna.upper()}]"
        if tag in texto_base:
            texto_base = texto_base.replace(tag, str(df[coluna].iloc[0]))  # Substitui a tag pela primeira linha da coluna
    return texto_base

# Função principal do Streamlit
def app():
    st.title('Gerador de Relatório Processual')

    # Carregar a planilha
    df = carregar_planilha()
    if df is not None:
        st.write("Planilha carregada com sucesso!")
        st.write("Colunas encontradas na planilha:")
        st.write(df.columns.tolist())

        # Entrar com o texto base
        texto_base = st.text_area("Insira o texto base do relatório", 
                                  "Trata-se de [TIPO DE AÇÃO] ajuizada por [AUTOR] contra [RÉU]...")

        # Exibir as colunas como tags
        colunas_selecionadas = []
        for coluna in df.columns:
            if st.checkbox(f"Adicionar {coluna} ao texto", value=True):
                colunas_selecionadas.append(coluna)

        if st.button("Gerar Relatório"):
            if colunas_selecionadas:
                # Substituir as tags pelas colunas selecionadas
                relatorio = gerar_relatorio(df[colunas_selecionadas], texto_base)
                st.write("Relatório Gerado:")
                st.write(relatorio)
            else:
                st.warning("Por favor, selecione pelo menos uma coluna.")
    
if __name__ == "__main__":
    app()
