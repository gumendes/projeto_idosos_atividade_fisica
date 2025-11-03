
import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIGURAÇÕES INICIAIS
# ==============================
st.set_page_config(
    page_title="Atividades Físicas — Idosas",
    page_icon="🏃‍♀️",
    layout="wide"
)

st.title("🏃‍♀️ Projeto — Incentivo às Práticas de Atividades Físicas por Idosos")
st.markdown("""
Este dashboard foi desenvolvido para apoiar o acompanhamento das alunas que 
participam das atividades físicas na **Praça Zumbi dos Palmares (São Paulo)**.  
Ele permite visualizar dados de presença, satisfação, gamificação e previsões de faltas.
""")

# ==============================
# CARREGAMENTO DE DADOS
# ==============================
@st.cache_data
def carregar_dados():
    dados = pd.read_excel("data/dados_idosos_simulados_v2.xlsx")
    try:
        ranking = pd.read_csv("data/ranking_gamificacao.csv")
    except:
        ranking = None
    try:
        previsoes = pd.read_csv("data/previsoes_faltas.csv")
    except:
        previsoes = None
    return dados, ranking, previsoes

dados, ranking, previsoes = carregar_dados()

# ==============================
# FILTROS
# ==============================
st.sidebar.header("🔍 Filtros")
atividades = sorted(dados["atividade"].unique())
atividade_sel = st.sidebar.multiselect("Selecione as atividades:", atividades, default=atividades)

dias_semana = sorted(dados["dia_semana"].unique())
dias_sel = st.sidebar.multiselect("Selecione os dias da semana:", dias_semana, default=dias_semana)

dados_filtrados = dados[
    (dados["atividade"].isin(atividade_sel)) &
    (dados["dia_semana"].isin(dias_sel))
]

# ==============================
# MÉTRICAS PRINCIPAIS
# ==============================
col1, col2, col3 = st.columns(3)
taxa_presenca = dados_filtrados["presenca"].mean() * 100
media_satisfacao = dados_filtrados["satisfacao"].mean()
total_participacoes = len(dados_filtrados[dados_filtrados["presenca"] == 1])

col1.metric("🎯 Taxa média de presença", f"{taxa_presenca:.1f}%")
col2.metric("💬 Satisfação média", f"{media_satisfacao:.2f}/5")
col3.metric("👟 Total de participações", total_participacoes)

st.markdown("---")

# ==============================
# GRÁFICOS DE ANÁLISE
# ==============================
st.subheader("📈 Análise de Presença e Engajamento")

col_g1, col_g2 = st.columns(2)

# Gráfico 1 — Presença por dia da semana
pres_dia = dados_filtrados.groupby("dia_semana")["presenca"].mean().reset_index()
fig1 = px.bar(pres_dia, x="dia_semana", y="presenca",
              title="Presença Média por Dia da Semana", text_auto=".2f",
              color="presenca", color_continuous_scale="tealgrn")
col_g1.plotly_chart(fig1, use_container_width=True)

# Gráfico 2 — Presença por tipo de atividade
pres_ativ = dados_filtrados.groupby("atividade")["presenca"].mean().reset_index()
fig2 = px.bar(pres_ativ, x="atividade", y="presenca",
              title="Presença Média por Tipo de Atividade", text_auto=".2f",
              color="presenca", color_continuous_scale="purpor")
col_g2.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ==============================
# GAMIFICAÇÃO
# ==============================
st.subheader("🏅 Ranking Gamificado")

if ranking is not None:
    st.dataframe(ranking.head(10), use_container_width=True)
else:
    st.info("O ranking de gamificação ainda não foi gerado. Execute o notebook 02_gamificacao_e_visualizacoes.ipynb para criá-lo.")

st.markdown("---")

# ==============================
# MODELO PREDITIVO
# ==============================
st.subheader("🤖 Previsões de Faltas")

if previsoes is not None:
    st.markdown("Estas são as alunas com **maior probabilidade de faltar** nas próximas aulas:")
    previsoes_top = previsoes.sort_values("prob_falta", ascending=False).head(10)
    st.dataframe(previsoes_top, use_container_width=True)

    st.markdown("💬 **Ações sugeridas:** enviar mensagens de incentivo para as alunas acima, reforçando o engajamento e o senso de pertencimento.")
else:
    st.info("O modelo preditivo ainda não foi treinado. Execute o notebook 03_modelo_preditivo.ipynb para gerar previsões.")

st.markdown("---")

# ==============================
# RODAPÉ
# ==============================
st.caption("""
Desenvolvido por **Gustavo Mendes** — Projeto de Conclusão do Curso de Ciência de Dados  
📍 Praça Zumbi dos Palmares — São Paulo | 2025
""")
