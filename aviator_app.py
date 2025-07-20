arquivo = st.file_uploader("📁 Envie seu arquivo CSV ou Excel", type=["csv", "xlsx"])

def carregar_dados(arquivo):
    if arquivo.name.endswith('.csv'):
        return pd.read_csv(arquivo)
    else:
        return pd.read_excel(arquivo)

if arquivo:
    df = carregar_dados(arquivo)
    st.success("Arquivo carregado com sucesso!")

    # Exibe os dados
    st.subheader("🔍 Visualização dos Dados")
    st.dataframe(df)

    # Padroniza o nome da coluna
    colunas = [c.lower() for c in df.columns]
    if 'multiplicador' in colunas:
        df.columns = colunas  # Renomeia as colunas para minúsculo
        st.subheader("📈 Estatísticas Básicas")
        st.metric("Média", round(df['multiplicador'].mean(), 2))
        st.metric("Máximo", df['multiplicador'].max())
        st.metric("Mínimo", df['multiplicador'].min())

        # Histograma
        st.subheader("📊 Distribuição dos Multiplicadores")
        fig, ax = plt.subplots()
        ax.hist(df['multiplicador'], bins=20, color='skyblue', edgecolor='black')
        st.pyplot(fig)

        # Gráfico de linha
        st.subheader("📉 Evolução dos Multiplicadores")
        st.line_chart(df['multiplicador'])

        # Sequências abaixo de 2.0
        st.subheader("⚠️ Padrões de Baixo Rendimento (< 2.0x)")
        sequencia = (df['multiplicador'] < 2.0).astype(int)
        contagem = (sequencia.diff() != 0).cumsum()
        grupos = sequencia.groupby(contagem).sum()
        maiores = grupos[grupos >= 3]
        st.write(f"Sequências com 3+ rodadas abaixo de 2.0x: {len(maiores)}")
        if not maiores.empty:
            st.write(maiores.reset_index(drop=True))
    else:
        st.warning("A coluna 'multiplicador' não foi encontrada.")
