import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
# Dividir a página em 2 colunas com proporções 1:3
col1, col2 = st.columns([1, 3])

# 1. Carrega os dados do arquivo CSV local
@st.cache_data  # Cache para melhor performance
def load_data():
    try:
        # Converter durante a leitura (para colunas específicas)
        df = pd.read_csv(
            "prazos_audiencias.csv",
            thousands='.',          # Define o PONTO como separador de milhar
            decimal=',',            # Define a VÍRGULA como decimal (opcional para Brasil)
            encoding='utf-8'        # Garante compatibilidade com caracteres especiais
        )
       
        return df
    except FileNotFoundError:
        st.error("Arquivo 'prazos_audiencias.csv' não encontrado na pasta do app!")
        st.stop()

# 2. Uso no seu código (substitua a parte do Google Sheets)
df = load_data()

varas = ["ARARANGUÁ","1VT BALNEÁRIO CAMBORIÚ","2VT BALNEÁRIO CAMBORIÚ","1VT BLUMENAU","2VT BLUMENAU","3VT BLUMENAU","4VT BLUMENAU","1VT BRUSQUE","2VT BRUSQUE","CAÇADOR","CANOINHAS",
         "1VT CHAPECÓ","2VT CHAPECÓ","3VT CHAPECÓ","4VT CHAPECÓ","CONCÓRDIA","1VT CRICIÚMA","2VT CRICIÚMA","3VT CRICIÚMA","CURITIBANOS","1VT FLORIANÓPOLIS",
         "2VT FLORIANÓPOLIS","3VT FLORIANÓPOLIS","4VT FLORIANÓPOLIS","5VT FLORIANÓPOLIS","6VT FLORIANÓPOLIS","7VT FLORIANÓPOLIS","FRAIBURGO","IMBITUBA","INDAIAL",
         "1VT ITAJAÍ","2VT ITAJAÍ","3VT ITAJAÍ","ITAPEMA","1VT JARAGUÁ DO SUL","2VT JARAGUÁ DO SUL","JOAÇABA","1VT JOINVILLE","2VT JOINVILLE","3VT JOINVILLE","4VT JOINVILLE",
         "5VT JOINVILLE","1VT LAGES","2VT LAGES","3VT LAGES","MAFRA","NAVEGANTES","PALHOÇA","1VT RIO DO SUL","2VT RIO DO SUL","SÃO BENTO DO SUL","1VT SÃO JOSÉ","2VT SÃO JOSÉ",
         "3VT SÃO JOSÉ","SÃO MIGUEL DO OESTE","TIMBÓ","1VT TUBARÃO","2VT TUBARÃO","VIDEIRA","XANXERÊ"]

tipo = ["Inicial/Conciliação","Una","Instrução"]

vara_mapping = {}

# Ajusta o número índice da vara para se adequar ao índice da página das agendas    
def create_vara_mapping():
    for i, vara in enumerate(varas):
        vara_mapping[vara] = str(i)

# Obtem o índice da vara escolhida
def get_vara_index():
    selected_vara = vara
    if selected_vara == "Selecione uma Vara" or selected_vara not in varas:
        st.error.alert(
            text="Por favor, selecione uma Vara do Trabalho.",
            title="Nenhuma Vara Selecionada",
            button="OK"
        )
        return None
    
    # Certifica-se que o mapeamento está criado
    if not vara_mapping:
        create_vara_mapping()
    
    return vara_mapping[selected_vara]

# ----- Coluna da esquerda------

with col1:
    st.image("images/corina.png", width=120)
    #st.title('Preencha os dados')
    vara = st.selectbox('Selecione a Vara', varas)
    tipo_aud = st.selectbox('Selecione o tipo de audiência', tipo)
    pz_atual = st.text_input(label="Informe o **PRAZO ATUAL** (em dias corridos) de designação de audiências, conforme relatório do [Illumina12](https://app.powerbi.com/reportEmbed?ctid=ccd9917e-cb47-42a5-a262-e2272dcef6ab&autoAuth=true&navContentPaneEnabled=false&reportId=deb0d4be-ca8d-48a6-a55c-05df2b04e0f8&pageName=ReportSectionfb443df15e48345bb898), aba 'DT mais distante':", placeholder="Prazo máximo atual")
    qtd_aud = st.text_input(label="Informe a **QUANTIDADE ATUAL** de **AUDIÊNCIAS** designadas, conforme relatório do [Illumina12](https://app.powerbi.com/reportEmbed?ctid=ccd9917e-cb47-42a5-a262-e2272dcef6ab&autoAuth=true&navContentPaneEnabled=false&reportId=deb0d4be-ca8d-48a6-a55c-05df2b04e0f8&pageName=ReportSectionfb443df15e48345bb898), aba 'Qtd. Designadas':", placeholder="Quantidade atual")
    novos = st.text_input(label="Informe a **QUANTIDADE ATUAL** de **PROCESSOS** novos por mês no conhecimento - Quadro 'Recebidos no conhecimento' do Painel principal do [Illumina12](https://app.powerbi.com/groups/2f01f6c2-13bb-436e-a45b-6b108615a343/reports/e740b81c-2d77-416e-99c8-ae9b2ba639f3/40139b5c364672d35d8a?ctid=ccd9917e-cb47-42a5-a262-e2272dcef6ab&experience=power-bi):", placeholder="processos novos mensais")
    percent = st.text_input(label="Informe o percentual, em média, de processos que vão para a pauta, sem o sinal %:", placeholder="Percentual. Apenas número")
    qtd_nova = st.text_input(label="Informe a quantidade de audiências que **SERÃO** designadas semanalmente:", placeholder="Quantidade nova semanal")

# ------ Validação dos Inputs ------
inputs_obrigatorios = {
    "Vara": vara,
    "Tipo de audiência": tipo_aud,
    "Prazo atual": pz_atual,
    "Quantidade atual de audiências": qtd_aud,
    "Processos novos mensais": novos,
    "Percentual para pauta": percent,
    "Nova quantidade semanal": qtd_nova
}

# Na parte onde você captura os inputs, converta para números:
try:
    prazo_num = int(pz_atual) if pz_atual else 0
    qtd_aud_num = int(qtd_aud) if qtd_aud else 0
    novos_num = int(novos) if novos else 0
    percent_num = float(percent) if percent else 0
    qtd_nova_num = int(qtd_nova) if qtd_nova else 0
    novos_pauta_sem_num = math.ceil((novos_num * (percent_num / 100)) / 4)
except ValueError:
    st.error("Por favor, insira valores **numéricos** válidos nos campos")
    st.stop()

# ------ Página central ----

with col2: 
    st.title("Adequação da pauta de audiências")
    st.write("")
    st.write("De acordo com o Provimento, os prazos máximos de designação de audiências da unidade são:")

    # Obtém o índice da vara selecionada
    vara_index = get_vara_index()

    # Se uma vara válida foi selecionada, mostra apenas a linha correspondente
    if vara_index:
        # Converte para inteiro 
        row_index = int(vara_index)
        # Verifica se o índice está dentro do range do DataFrame
        if row_index < len(df):
            # Mostra a linha correspondente
            st.dataframe(df.iloc[[row_index]], hide_index=True)
            st.write("*No provimento os prazos são em meses, mas aqui para facilitar os cálculos foram considerados em dias corridos.")
                        
            # Cria as variáveis com os valores das colunas 3, 4 e 5 (índices 2, 3 e 4 em Python)
            col3_valor = df.iloc[row_index, 2]  # Coluna 3 (índice 2)
            col4_valor = df.iloc[row_index, 3]  # Coluna 4 (índice 3)
            col5_valor = df.iloc[row_index, 4]  # Coluna 5 (índice 4)
            
            # atribuir a variáveis globais para usar em outras partes do código
            global inicial_prov, una_prov, instr_prov
            inicial_prov = col3_valor
            una_prov = col4_valor
            instr_prov = col5_valor
            
            # função para obter o prazo por tipo
            def obter_valor_por_tipo(tipo_selecionado):
                if tipo_selecionado == "Inicial/Conciliação":
                    return inicial_prov
                elif tipo_selecionado == "Una":
                    return una_prov
                elif tipo_selecionado == "Instrução":
                    return instr_prov
                return None

            if vara_index and tipo_aud:
                valor_resultante = obter_valor_por_tipo(tipo_aud)
                pzo_aud_select = int(valor_resultante)                

            # Verifica se algum campo obrigatório está vazio ou zero
            erros = []
            for campo, valor in inputs_obrigatorios.items():
                if not valor:
                    erros.append(f"⚠️ Favor inserir valor numérico em {campo}.")
                elif campo not in ["Vara", "Tipo de audiência"]:  # Campos que não são numéricos
                    try:
                        if float(valor) == 0:
                            erros.append(f"⚠️ {campo} não pode ser zero")
                    except ValueError:
                        erros.append(f"⚠️ {campo} deve ser um número válido")

            # Se houver erros, exibe todos e interrompe
            if erros:
                for erro in erros:
                    st.error(erro)
                st.stop()

            pz_atual_sem = prazo_num / 7
            qtd_adequar = qtd_nova_num * (pzo_aud_select / 7)
            novos_acum = (novos_pauta_sem_num - (qtd_nova_num - (qtd_aud_num/(prazo_num/7))))*(prazo_num/7)
            tx_red = (qtd_nova_num - novos_pauta_sem_num)
            tp_red_novos = (novos_acum-qtd_adequar) / tx_red        
            
            if (pz_atual_sem + tp_red_novos) < ((prazo_num - pzo_aud_select)/7):
                tp_red_tot_sem = (prazo_num - pzo_aud_select)/7
            else:
                tp_red_tot_sem = pz_atual_sem + tp_red_novos

            if (tp_red_tot_sem * 7) < (prazo_num - pzo_aud_select):
                tp_red_tot_dias = (prazo_num - pzo_aud_select)
            else:
                tp_red_tot_dias = tp_red_tot_sem * 7
            
            tp_red_tot_meses = tp_red_tot_dias / 30
            aud_atual_sem = math.ceil(qtd_aud_num / pz_atual_sem)
            aud_aumento_semanal = qtd_nova_num - aud_atual_sem

            # 1. Data atual
            data_atual = datetime.now().date()  # Apenas a data, sem horário

            # 2. Somar os dias
            data_futura = data_atual + timedelta(days=tp_red_tot_dias)

            # Limites do recesso (19/12 a 20/01 do ano seguinte)
            ano_recesso = data_futura.year
            inicio_recesso = datetime(ano_recesso, 12, 19).date()
            fim_recesso = datetime(ano_recesso + 1, 1, 20).date()

            # Verifica se a data da conformidade está no recesso ou após       
            if (data_futura.year == data_atual.year and data_futura.month == 12 and data_futura.day >= 19) or (data_futura.year > data_atual.year):
                data_futura += timedelta(days=30)
                tp_red_tot_sem = tp_red_tot_sem + 4
                tp_red_tot_dias = tp_red_tot_dias + 30
                tp_red_tot_meses = tp_red_tot_meses + 1
                texto_recesso = "*Foi descontado o recesso."
                mensagem = f"**A partir dos dados preenchidos à esquerda, com a nova quantidade de audiências semanais, a unidade estará em conformidade com o Provimento aproximadamente em:** {data_futura.strftime('%d/%m/%Y')}. Foi descontado o recesso 🎄, mas não há desconto de afastamentos."
            else:
                texto_recesso = ""
                mensagem = f"**A partir dos dados preenchidos à esquerda, com a nova quantidade de audiências semanais, a unidade estará em conformidade com o Provimento aproximadamente em:** {data_futura.strftime('%d/%m/%Y')}. Não há desconto de afastamentos."

            st.success(mensagem)
            
            st.subheader("Resumo")
            st.write(f"Atualmente são realizadas, em média, {aud_atual_sem} audiências por semana na unidade.")
            st.write(f"Aumentando de {aud_atual_sem} para {qtd_nova_num} audiências, haverá incremento de {aud_aumento_semanal} por semana.")
            st.write(f"Com isso, a unidade estará em conformidade com o prazo do Provimento em aproximadente {tp_red_tot_sem:.2f} semanas, ou {tp_red_tot_dias:.0f} dias, ou {tp_red_tot_meses:.2f} meses. {texto_recesso}")       
            
            st.divider()  # Barra horizontal padrão            
            st.subheader("Como o cálculo é feito")
            st.write(
                """ 
                Os cálculos consideram a quantidade total de audiências que já estão designadas e que não serão antecipadas. Considera também a quantidade de processos que semanalmente chegam para serem incluídos em pauta. \n
                A ideia é aumentar a quantidade atual de audiências designadas por semana para poder reduzir o prazo máximo.                 
                """                
            )
            st.write(f"Se hoje há {qtd_aud_num} audiências designadas em um prazo máximo de {prazo_num} dias, quer dizer que em média são designadas {aud_atual_sem} audiências por semana.")
            st.write(f"Como atualmente estão chegando {novos_pauta_sem_num} processos novos para incluir em pauta, estão sendo incluídos ao final do prazo.")
            st.write(f"No entanto, se aumentar a quantidade semanal de {aud_atual_sem} para {qtd_nova_num}, poderá incluir {aud_aumento_semanal} dos {novos_pauta_sem_num} que chegam novos, sobrando {novos_pauta_sem_num - aud_aumento_semanal} semanalmente para serem incluídos ao final.")
            st.write(f"Como as audiências já marcadas não serão antecipadas, ao final de {prazo_num} dias, todas as {qtd_aud_num} audiências serão realizadas, sobrando o acumulado de {novos_acum:.0f} audiências ({novos_pauta_sem_num - aud_aumento_semanal} X {prazo_num} / 7).")
            st.write(f"Como continuam sendo designadas {qtd_nova_num} audiências por semana, e a quantidade nova que chega semanalmente é menor que essa quantia ({novos_pauta_sem_num}), são antecipadas {aud_aumento_semanal} audiências por semana, que antes eram marcadas ao final.") 
            st.write(f"Assim, a unidade precisará de aproximadente {tp_red_tot_sem:.2f} semanas, ou {tp_red_tot_dias:.0f} dias, ou {tp_red_tot_meses:.2f} meses para se adequar ao Provimento.")

        else:
            st.error("Vara não encontrada no banco de dados.")
    else:
        st.warning("Selecione uma vara válida para visualizar os dados.")
