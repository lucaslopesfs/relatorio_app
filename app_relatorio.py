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
    # Cria uma lista para armazenar os relatórios gerados
    relatórios = []
    
    # Iterar sobre cada linha da planilha e gerar o relatório
    for index, row in df.iterrows():
        texto = texto_base
        for coluna in df.columns:
            tag = f"[{coluna.upper()}]"
            if tag in texto:
                texto = texto.replace(tag, str(row[coluna]))  # Substitui a tag pelo valor correspondente da linha
        relatórios.append(texto)
    
    # Adiciona os relatórios ao DataFrame como uma nova coluna
    df['Relatório Final'] = relatórios
    return df

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
                # Gerar os relatórios para todas as linhas
                df_com_relatorio = gerar_relatorio(df[colunas_selecionadas], texto_base)
                
                st.write("Relatório Gerado com sucesso!")
                st.write(df_com_relatorio[['Relatório Final']])

                # Permitir o download da planilha com os relatórios
                arquivo_saida = df_com_relatorio.to_excel(index=False)
                st.download_button(
                    label="Baixar Planilha com Relatórios",
                    data=arquivo_saida,
                    file_name="relatorios_gerados.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Por favor, selecione pelo menos uma coluna.")
    
if __name__ == "__main__":
    app()
