from dash import dcc
from dash import html
from dash import Dash
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

import sqlalchemy as db
import os
import pandas as pd
from datetime import datetime as dt
from textwrap import dedent

from dash_app.processs import (table_invest, graph_invest)

app = Dash(__name__, prevent_initial_callbacks=True, suppress_callback_exceptions=True)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Img(src="assets/images.jpg", className="app__logo"),
                html.H4("WALL STREET AND FRIENDS", className="header__text"),
            ],
            className="app__header",
        ),
        html.Div(
            [
                dcc.Tabs(
                    id="tabs",
                    value="_form",
                    children=[
                        dcc.Tab(
                            label="FORM",
                            id="_form_",
                            value="_form",
                            children=[
                                html.Div(
                                    [
                                        html.H5(
                                            "ABOUT YOU",
                                            className="section__heading",
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Full Name *",
                                                    className="input__heading",
                                                ),
                                                dcc.Input(
                                                    id="enter-full-name",
                                                    type="text",
                                                    className="fullname__input",
                                                    placeholder="e.g. Randolf Lazzaretti",
                                                ),
                                            ],
                                            className="input__container",
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Location *",
                                                    className="input__heading",
                                                ),
                                                dcc.Input(
                                                    id="enter-location",
                                                    type="text",
                                                    className="location__input",
                                                    placeholder="e.g. Miami",
                                                ),
                                            ],
                                            className="input__container",
                                        ),
                                        html.H5(
                                            "ABOUT YOUR INVESTMENT",
                                            className="section__heading",
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Investment Option Name *",
                                                    className="input__heading",
                                                ),
                                                dcc.Input(
                                                    id="enter-invest-name",
                                                    type="text",
                                                    className="invest__input",
                                                ),
                                            ],
                                            className="input__container",
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Daily yield (%) *",
                                                    className="input__heading",
                                                ),
                                                dcc.Input(
                                                    id="enter-daily-yield",
                                                    type="number",
                                                    min=0,
                                                    className="dailyyield__input",
                                                ),
                                            ],
                                            className="input__container",
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Term (in days) *",
                                                    className="input__heading",
                                                ),
                                                dcc.Input(
                                                    id="enter-term",
                                                    type="number",
                                                    min=0,
                                                    step=1,
                                                    className="term__input",
                                                ),
                                            ],
                                            className="input__container",
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Initial amount ($) *",
                                                    className="input__heading",
                                                ),
                                                dcc.Input(
                                                    id="enter-initial-amount",
                                                    type="number",
                                                    min=1,
                                                    className="initialamount__input",
                                                ),
                                            ],
                                            className="input__container",
                                        ),
                                        html.Br(),
                                        html.Button(
                                            "SUBMIT",
                                            id="submit-entry",
                                            className="submit__button",
                                            n_clicks=0,
                                        ),
                                    ],
                                    id="form", className="container__1"
                                ),
                            ],
                        ),
                        dcc.Tab(
                            label="RESULT",
                            id="_result",
                            value="_results",
                            children=[
                                html.Div(id="report"),
                            ],
                        ),
                    ],
                )
            ],
            className="tabs__container",
        ),
    ],
    className="app__container", id="printmeplease",
)


def register_callbacks1(dashapp):
    # SQL engine
    USERNAME = os.getenv("USERNAME")
    DBPW = os.getenv("DBPW")
    DBNAME = os.getenv("DBNAME")

    engine = db.create_engine(f'mysql+pymysql://{USERNAME}:{DBPW}@username.mysql.pythonanywhere-services.com/{DBNAME}')
    #engine = db.create_engine(f'mysql+pymysql://{USERNAME}:{DBPW}@icos.mysql.pythonanywhere-services.com/{DBNAME}', pool_recycle=280)
    connection = engine.connect()
    metadata = db.MetaData()

    SQL_form_table = db.Table(
         "form_data",
         metadata,
         db.Column("name", db.String(255)),
         db.Column("location", db.String(255)),
         db.Column("invest_option_name", db.String(255)),
         db.Column("yield", db.Float()),
         db.Column("term", db.Integer()),
         db.Column("init_amount", db.Float()),
         db.Column("time_stamp", db.String(255)),
    )

    @dashapp.callback(
        [
            Output("report", "children"),
        ],
        [
            Input('submit-entry', 'n_clicks'),
        ],
        [
            State("enter-full-name", "value"),
            State("enter-location", "value"),
            State("enter-invest-name", "value"),
            State("enter-daily-yield", "value"),
            State("enter-term", "value"),
            State("enter-initial-amount", "value"),
        ],
    )
    def report_screen(submit_entry,
            full_name,
            location,
            invest_name,
            daily_yield,
            term,
            initial_amount
    ):

        if (
                full_name is None
                or location is None
                or invest_name is None
                or daily_yield is None
                or term is None
                or initial_amount is None
        ):
            report_invest = html.Div(children=[])

            return report_invest

        else:
            sample_entry = [
                {
                    "name": full_name,
                    "location": location,
                    "invest_option_name": invest_name,
                    "yield": daily_yield,
                    "term": term,
                    "init_amount": initial_amount,
                    "time_stamp": dt.now(),
                }
            ]

            insert_entry = connection.execute(db.insert(SQL_form_table), (sample_entry))

            df = pd.read_sql_query(
                dedent(
                    """
            SELECT * FROM form_data ORDER BY id DESC LIMIT 1;
            """
                ),
                engine,
            )
            full_name = df.iloc[0, 0]
            location = df.iloc[0, 1]
            invest_name = df.iloc[0, 2]
            daily_yield = df.iloc[0, 3]
            term = df.iloc[0, 4]
            initial_amount = df.iloc[0, 5]

            tabela = table_invest(daily_yield, term, initial_amount)
            grafico = graph_invest(invest_name, full_name, tabela)

            report_invest = html.Div([
                dcc.Graph(id='grafico-invest', figure=grafico)
            ])

            return report_invest

    engine.dispose()

if __name__ == '__main__':
     app.run_server(debug=True)