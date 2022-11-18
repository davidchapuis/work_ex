import pandas as pd
import plotly.express as px

def table_invest(daily_yield, term, initial_amount):
    height = term + 1
    tabelaa = pd.DataFrame(1, index=range(int(height)), columns=["Days"])

    tabelaa["Balance ($)"] = 0.00
    i = 0
    for i in range(len(tabelaa)):
        if i == 0:
            tabelaa["Balance ($)"] = initial_amount
            i = i + 1
        else:
            if i < int(height):
                tabelaa["Balance ($)"][i] = tabelaa.iloc[i - 1, 1] * (1+daily_yield)
                i = i + 1
    return tabelaa

# traçage de la courbe pour pays autre, particules 2.5
def graph_invest(invest_name, full_name, tabela):
    graff = px.line(tabela, x="Days", y="Balance ($)")
    graff.layout.font = dict(family="Helvetica")
    graff.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
                                margin=dict(l=1, r=1, b=10, t=130), title=f"{invest_name}: investment balance ($) for {full_name}")
    return graff