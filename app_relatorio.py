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
            tag = f"[{coluna.upper()}]"  # A tag é convertida para maiúsculo
            if tag in texto:
                texto = texto.replace(tag, str(row[coluna]))  # Substitui a tag pelo valor correspondente da linha
        relatórios.append(texto)
    
    # Adiciona os relatórios ao DataFrame como uma nova coluna
    df['Relatório Final'] = relatórios
    return df

# Função principal do Streamlit
def app():
    # Definir título e ícone
    st.set_page_config(page_title="Gerador de Relatório Processual", page_icon="📑")
    st.title("Gerador de Relatório Processual 📑")
    
    # Introdução detalhada
    st.markdown("""
    **Bem-vindo ao Gerador de Relatório Processual!** 📝
    
    Este aplicativo foi criado para gerar relatórios processuais de maneira automática a partir de uma planilha de auditoria. Você só precisa fazer o upload da sua planilha, preencher o texto base do relatório e gerar o relatório final.
    
    ### Como usar:
    1. **Faça o upload da sua planilha Excel.** A planilha deve conter dados que você deseja incluir no relatório (como informações sobre processos, partes envolvidas, etc.).
    2. **Preencha o texto base do relatório.** Use as tags, como [TIPO DE AÇÃO], para indicar onde você quer que as informações da planilha sejam inseridas.
    3. **Selecione as colunas da planilha.** Escolha as colunas da sua planilha que você deseja incluir nas tags.
    4. **Gere o relatório.** Clique no botão "Gerar Relatório" para ver a pré-visualização do relatório gerado e, em seguida, baixe a planilha com os dados originais e o relatório gerado.
    
    ### Exemplo de Tags:
    - [TIPO DE AÇÃO]: será substituído pela coluna "TIPO DE AÇÃO" da sua planilha.
    - [AUTOR]: será substituído pela coluna "AUTOR" da sua planilha.
    """)

    # Carregar a planilha
    df = carregar_planilha()
    if df is not None:
        st.success("Planilha carregada com sucesso!")

        # Exibir as colunas da planilha em uma caixa rolável
        st.subheader("Colunas encontradas na planilha:")
        st.text("Essas são as colunas que você pode utilizar nas tags do seu relatório.")
        st.write(df.columns.tolist())

        # Entrada do texto base
        texto_base = st.text_area(
            "Insira o texto base do relatório",
            "Trata-se de [TIPO DE AÇÃO] ajuizada por [AUTOR] contra [RÉU]..."
        )

        # Exibição de colunas para seleção
        st.subheader("Selecione as colunas para incluir nas tags:")
        colunas_selecionadas = []
        for coluna in df.columns:
            if st.checkbox(f"Adicionar {coluna} ao texto", value=True):
                colunas_selecionadas.append(coluna)

        # Botão para gerar o relatório
        if st.button("Gerar Relatório"):
            if colunas_selecionadas:
                # Gerar o relatório com base nas colunas selecionadas
                df_com_relatorio = gerar_relatorio(df, texto_base)
                
                st.success("Relatório gerado com sucesso!")

                # Exibir as primeiras linhas do relatório gerado
                st.subheader("Pré-visualização do Relatório Final:")
                st.write(df_com_relatorio[['Relatório Final']].head())

                # Permitir o download da planilha com os relatórios e dados originais
                arquivo_saida = df_com_relatorio.to_excel(index=False)
                st.download_button(
                    label="Baixar Planilha com Relatórios e Dados Originais",
                    data=arquivo_saida,
                    file_name="relatorios_gerados_com_dados.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("Por favor, selecione pelo menos uma coluna para incluir no relatório.")
    
    else:
        st.warning("Por favor, faça o upload de uma planilha para continuar.")
    
if __name__ == "__main__":
    app()
