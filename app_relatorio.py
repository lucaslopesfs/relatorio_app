import streamlit as st
import pandas as pd


def carregar_planilha():
    uploaded_file = st.file_uploader("Escolha a planilha de auditoria", type="xlsx")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        return df
    return None

# Função para criar o relatório a partir do texto base
def gerar_relatorio(df, texto_base):
    # Substitui as "tags" pelo conteúdo da planilha
    for col in df.columns:
        texto_base = texto_base.replace(f"[{col.upper()}]", str(df[col].iloc[0]))  # Substitui pelo valor da primeira linha
    return texto_base

# Função para gerar a planilha final com os relatórios
def gerar_planilha_com_relatorio(df, texto_base):
    relatorios = []
    for index, row in df.iterrows():
        texto_relatorio = texto_base
        for col in df.columns:
            texto_relatorio = texto_relatorio.replace(f"[{col.upper()}]", str(row[col]))  # Substitui pela linha atual
        relatorios.append(texto_relatorio)
    
    df['Relatório Final'] = relatorios  # Adiciona a coluna com o relatório final
    return df

# Carregar a planilha
df = carregar_planilha()

# Se a planilha for carregada com sucesso
if df is not None:
    st.write("Dados da Planilha:", df.head())

    # Campo para inserir o texto base
    texto_base = st.text_area("Insira o texto base para o relatório", "Trata-se de [TIPO DE AÇÃO] ajuizada por [AUTOR] contra [RÉU]...")

    if texto_base:
        st.write("Texto inserido:", texto_base)

        # Gerar os relatórios
        df_com_relatorios = gerar_planilha_com_relatorio(df, texto_base)

        # Exibir a planilha com os relatórios
        st.write("Planilha com os Relatórios:", df_com_relatorios)

        # Baixar a planilha com os relatórios
        st.download_button(
            label="Baixar Planilha com Relatórios",
            data=df_com_relatorios.to_excel(index=False, engine='openpyxl'),
            file_name="relatorios_completos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
