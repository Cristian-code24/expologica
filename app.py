from html import escape

import streamlit as st

from boolean_logic import LAWS, truth_table
from circuit_canvas import render_circuit
from course_references import list_references, read_reference
from exercises import CIRCUITS, EXERCISES, exercise_tables
from visual_assets import find_visual_asset, image_data_uri


st.set_page_config(
    page_title="Compuertas lógicas · Grupo ®✓",
    page_icon="⌁",
    layout="wide",
    initial_sidebar_state="expanded",
)

SLIDES = [
    ("Portada", "cover"),
    ("Ruta de la clase", "index"),
    ("¿Qué hace una compuerta?", "definition"),
    ("Álgebra de Boole", "algebra"),
    ("Compuerta NOT", "NOT"),
    ("Compuerta AND", "AND"),
    ("Compuerta OR", "OR"),
    ("Compuertas derivadas", "derived"),
    ("Leyes y teoremas", "laws"),
    ("Ejercicio 5.11a", "5.11a"),
    ("Ejercicio 5.11b", "5.11b"),
    ("Ejercicio 5.12 · NAND", "5.12"),
    ("Ejercicio 5.13 · NOR", "5.13"),
    ("Material de consulta", "references"),
    ("Cierre", "closing"),
]

ROUTE_STATIONS = [
    {
        "range": "01–04",
        "title": "Contexto y lenguaje",
        "summary": "Proposiciones, V/F y señales 1/0.",
        "concept": "Verdadero corresponde a 1 y Falso a 0; los operadores lógicos se implementan con compuertas.",
    },
    {
        "range": "05–08",
        "title": "Compuertas",
        "summary": "Cada compuerta tiene una regla.",
        "concept": "La regla de la compuerta determina la salida para cada combinación de entradas.",
    },
    {
        "range": "09",
        "title": "Leyes booleanas",
        "summary": "Equivalencias sin cambiar la función.",
        "concept": "Las equivalencias simplifican expresiones sin cambiar sus resultados.",
    },
    {
        "range": "10–13",
        "title": "Ejercicios",
        "summary": "De la expresión al circuito.",
        "concept": "La tabla verifica la función y el circuito muestra su implementación.",
    },
    {
        "range": "14–15",
        "title": "Fuentes y cierre",
        "summary": "Fuentes y síntesis.",
        "concept": "Las fuentes respaldan la notación y las representaciones completan el análisis.",
    },
]


def _move_to(index: int) -> None:
    index = max(0, min(index, len(SLIDES) - 1))
    st.session_state.slide_index = index
    st.session_state.nav_select = index


def _previous() -> None:
    _move_to(st.session_state.slide_index - 1)


def _next() -> None:
    _move_to(st.session_state.slide_index + 1)


def _sync_navigation() -> None:
    st.session_state.slide_index = st.session_state.nav_select


def _move_route_back() -> None:
    st.session_state.route_step = max(0, st.session_state.route_step - 1)


def _move_route_forward() -> None:
    st.session_state.route_step = min(
        len(ROUTE_STATIONS) - 1, st.session_state.route_step + 1
    )


if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0
if "nav_select" not in st.session_state:
    st.session_state.nav_select = 0
if "route_step" not in st.session_state:
    st.session_state.route_step = 0


st.markdown(
    """
    <style>
    :root { --teal:#5be3c2; --muted:#9bb2bf; --violet:#a78bfa; --coral:#ffb36b; }
    .stApp { background:
      radial-gradient(ellipse at 86% 2%, rgba(69,92,196,.23), transparent 35%),
      radial-gradient(ellipse at 8% 50%, rgba(19,136,157,.12), transparent 38%),
      linear-gradient(155deg,#081321 0%,#0b1727 52%,#11162b 100%); }
    @keyframes slideReveal { from { opacity:0; transform:translateY(8px); }
      to { opacity:1; transform:translateY(0); } }
    @keyframes heroZoom { from { transform:scale(1.02); } to { transform:scale(1.1); } }
    @keyframes logoFloat { 0%,100% { transform:translateY(0) rotate(-1deg); }
      50% { transform:translateY(-8px) rotate(1deg); } }
    @keyframes guideBob { 0%,100% { transform:translate(-50%,0); }
      50% { transform:translate(-50%,-8px); } }
    @keyframes lightSweep { 0% { opacity:.15; transform:translateX(-110%); }
      45%,100% { opacity:0; transform:translateX(110%); } }
    [data-testid="stMainBlockContainer"] { animation:slideReveal .36s ease-out both; }
    @media (prefers-reduced-motion: reduce) {
      [data-testid="stMainBlockContainer"] { animation:none; }
    }
    [data-testid="stSidebar"] { background:rgba(7,17,31,.94); border-right:1px solid rgba(112,154,255,.2); }
    .eyebrow { color:#74dbc1; font-size:.72rem; letter-spacing:.18em; text-transform:uppercase; font-weight:700; }
    .hero-title { font-size:clamp(2.7rem,6vw,5.3rem); line-height:.98; font-weight:800;
      letter-spacing:-.055em; margin:.6rem 0 1.15rem; color:#f0f7f8; }
    .hero-title span { color:#65dfc2; }
    .hero-sub { color:#a5bac4; font-size:1.12rem; max-width:750px; line-height:1.75; }
    .hero-context { color:#c2d2d8; font-size:1.02rem; line-height:1.8; max-width:900px; }
    .slide-title { font-size:2.05rem; font-weight:750; letter-spacing:-.035em; margin:.25rem 0 .4rem; }
    .slide-lead { color:#9fb4bf; font-size:1.02rem; margin-bottom:1.15rem; }
    .info-card { padding:1.1rem 1.2rem; border:1px solid rgba(133,177,192,.18);
      border-radius:16px; background:rgba(16,34,47,.66); min-height:110px; }
    .info-card strong { color:#71e4c4; }
    .route-card { padding:1.15rem 1.25rem; border:1px solid rgba(133,177,192,.18);
      border-radius:16px; background:linear-gradient(145deg,rgba(16,34,47,.82),rgba(12,27,39,.72));
      min-height:195px; line-height:1.65; }
    .route-card strong { color:#71e4c4; }
    .concept-panel { padding:1rem 1.15rem; border-left:3px solid #5be3c2; border-radius:0 12px 12px 0;
      background:rgba(58,116,112,.12); color:#c6d6dc; line-height:1.75; }
    .law-card { padding:.95rem 1rem; border:1px solid rgba(133,177,192,.16);
      border-radius:14px; background:rgba(16,34,47,.64); min-height:140px; }
    .law-card strong { color:#71e4c4; }
    .member { color:#d5e2e6; padding:.28rem 0; border-bottom:1px solid rgba(136,169,181,.1); }
    .small-note { color:#91a8b4; font-size:.9rem; }
    div[data-testid="stMetric"] { background:rgba(17,37,48,.65); padding:14px 18px; border-radius:14px; }
    div[data-testid="stMetric"] label { color:#9bb2bf; }
    div[data-testid="stButton"] > button { border-radius:11px; }
    [data-testid="stMarkdownContainer"] .stLatex { color:#effaf7; }
    .stTabs [data-baseweb="tab-list"] { gap:.45rem; }
    .stTabs [data-baseweb="tab"] { border-radius:10px 10px 0 0; }
    .stButton > button { border:1px solid rgba(122,177,255,.28); color:#e7f2ff;
      background:linear-gradient(135deg,rgba(49,92,157,.42),rgba(94,57,153,.3));
      transition:transform .18s ease,border-color .18s ease,filter .18s ease; }
    .stButton > button:hover { transform:translateY(-2px); border-color:#70e8cf; filter:brightness(1.12); }
    [data-testid="stProgressBar"] > div > div > div > div { background:linear-gradient(90deg,#35d9bd,#8d7cff,#ffb36b); }
    .cover-hero { position:relative; isolation:isolate; display:grid; grid-template-columns:minmax(0,1fr) 220px;
      gap:1rem; min-height:380px; overflow:hidden; padding:clamp(1.5rem,4vw,3rem);
      border:1px solid rgba(196,218,255,.24); border-radius:26px;
      background:linear-gradient(135deg,#10243a,#172044 64%,#271e47); box-shadow:0 24px 70px rgba(0,0,0,.32); }
    .cover-hero::after { content:""; position:absolute; inset:0; z-index:0; pointer-events:none;
      background:linear-gradient(105deg,transparent 35%,rgba(154,214,255,.13) 50%,transparent 65%);
      animation:lightSweep 9s ease-in-out infinite; }
    .cover-backdrop { position:absolute; inset:-3%; z-index:-2; background-size:cover; background-position:center 47%;
      opacity:.8; animation:heroZoom 24s ease-in-out infinite alternate; }
    .cover-shade { position:absolute; inset:0; z-index:-1;
      background:linear-gradient(100deg,rgba(5,15,28,.96) 0%,rgba(7,20,37,.87) 45%,rgba(17,25,55,.52) 100%); }
    .cover-content,.cover-side { position:relative; z-index:1; }
    .cover-content { align-self:center; max-width:790px; }
    .cover-content .hero-title { font-size:clamp(2.1rem,4vw,3.8rem); margin:.5rem 0 1rem;
      overflow-wrap:normal; word-break:keep-all; }
    .cover-context { max-width:720px; margin:.7rem 0 1.15rem; color:#d5e4f2; font-size:1.02rem; line-height:1.7; }
    .cover-side { display:flex; flex-direction:column; align-items:center; justify-content:center; gap:1rem; }
    .school-logo { width:clamp(105px,13vw,158px); height:clamp(105px,13vw,158px); object-fit:contain; padding:9px;
      border:1px solid rgba(255,255,255,.72); border-radius:25px; background:#fff;
      box-shadow:0 16px 38px rgba(0,0,0,.24); animation:logoFloat 5s ease-in-out infinite; }
    .logo-fallback { width:130px; height:130px; display:grid; place-items:center; border-radius:25px;
      border:1px solid rgba(255,255,255,.75); color:#fff; font-size:2rem; font-weight:850;
      background:linear-gradient(145deg,#087e9d,#6e5ad8); }
    .boole-card { display:flex; align-items:center; gap:.75rem; width:min(100%,320px); padding:.75rem;
      border:1px solid rgba(219,232,255,.26); border-radius:18px; background:rgba(8,18,33,.76);
      color:#edf5ff; backdrop-filter:blur(8px); box-shadow:0 12px 30px rgba(0,0,0,.2); }
    .boole-portrait { width:88px; height:88px; flex:0 0 88px; object-fit:cover; object-position:32% center;
      border-radius:13px; border:1px solid rgba(255,255,255,.5); }
    .boole-placeholder { width:88px; height:88px; flex:0 0 88px; display:grid; place-items:center; border-radius:13px;
      background:linear-gradient(145deg,#183d59,#463574); font-size:1.55rem; }
    .boole-card strong { display:block; color:#87ead4; font-size:.92rem; }
    .boole-card span { display:block; color:#bdccdc; font-size:.78rem; line-height:1.4; }
    .group-heading { display:flex; align-items:center; gap:.75rem; margin:1.3rem 0 .35rem; }
    .group-mark { display:inline-grid; place-items:center; width:36px; height:36px; border-radius:12px;
      color:#07161f; font-weight:900; background:linear-gradient(135deg,#6be8ca,#7dbaff); }
    .members-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.65rem; margin:.8rem 0; }
    .member-card { display:flex; align-items:center; min-height:54px; padding:.75rem .9rem; border-radius:13px;
      border:1px solid rgba(154,188,255,.18); color:#e4edf8; font-size:.85rem;
      background:linear-gradient(135deg,rgba(23,46,72,.84),rgba(29,35,67,.78)); }
    .member-card::before { content:""; width:8px; height:8px; margin-right:.65rem; flex:0 0 8px; border-radius:50%;
      background:#66e4c8; box-shadow:0 0 12px rgba(102,228,200,.65); }
    .route-visual { position:relative; margin:.55rem 0 1rem; padding-top:76px;
      container-type:inline-size; container-name:route-cards; }
    .route-guide { position:absolute; z-index:2; top:0; width:58px; height:64px; display:grid; place-items:center;
      margin-left:-29px; animation:guideBob 1.9s ease-in-out infinite; transition:left .35s ease; }
    .route-guide svg { width:58px; height:64px; overflow:visible; filter:drop-shadow(0 6px 12px rgba(0,0,0,.3)); }
    .route-line { position:absolute; top:109px; left:9%; width:82%; height:4px; border-radius:99px;
      background:linear-gradient(90deg,#42dec3,#7e9cff,#bc82ff,#ffb56f); opacity:.75; }
    .route-stations { position:relative; display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:.65rem; }
    .route-station { position:relative; min-height:142px; padding:1.1rem .85rem .8rem; border:1px solid rgba(149,184,255,.2);
      border-radius:17px; background:linear-gradient(155deg,rgba(20,42,66,.94),rgba(23,29,55,.91));
      transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease; }
    .route-station.active { transform:translateY(3px); border-color:#6ce7ce;
      box-shadow:0 0 0 1px rgba(108,231,206,.22),0 12px 28px rgba(19,191,173,.14); }
    .route-station strong,.route-station span { word-break:normal; overflow-wrap:break-word; }
    .station-index { display:inline-grid; place-items:center; width:29px; height:29px; margin-bottom:.55rem;
      border-radius:10px; color:#071a26; font-size:.78rem; font-weight:850;
      background:linear-gradient(135deg,#6ce7ce,#9db7ff); }
    .route-station strong { display:block; color:#eef5ff; font-size:.83rem; }
    .route-station span { display:block; margin-top:.3rem; color:#aebfd2; font-size:.73rem; line-height:1.45; }
    .route-focus { display:flex; align-items:center; gap:.85rem; padding:1rem 1.1rem; margin:.5rem 0 1rem;
      border:1px solid rgba(105,225,205,.27); border-radius:15px;
      background:linear-gradient(100deg,rgba(25,114,124,.2),rgba(97,76,163,.16)); }
    .route-focus b { color:#70ead0; white-space:nowrap; }
    .route-focus span { color:#e2ecf6; }
    @container route-cards (max-width:650px) {
      .route-stations { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .route-line,.route-guide { display:none; }
      .route-visual { padding-top:0; }
      .route-station.active::after { content:"👆"; position:absolute; top:-1.55rem; left:50%;
        font-size:1.3rem; animation:guideBob 1.8s ease-in-out infinite; }
    }
    @media(max-width:850px) { .cover-hero { grid-template-columns:1fr; } .cover-side { flex-direction:row; }
      .members-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .route-stations { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .route-line,.route-guide { display:none; } .route-visual { padding-top:0; }
      .route-station.active::after { content:"👆"; position:absolute; top:-1.55rem; left:50%;
        font-size:1.3rem; animation:guideBob 1.8s ease-in-out infinite; } }
    @media(prefers-reduced-motion:reduce) {
      .cover-backdrop,.cover-hero::after,.school-logo,.route-guide,.route-station.active::after { animation:none; }
      .stButton > button,.route-station { transition:none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### GRUPO ®✓")
    st.caption("Compuertas lógicas · Álgebra de Boole")
    st.selectbox(
        "Navegación por diapositivas",
        options=range(len(SLIDES)),
        format_func=lambda i: f"{i + 1:02d} · {SLIDES[i][0]}",
        key="nav_select",
        on_change=_sync_navigation,
    )
    st.markdown("---")
    st.caption("Presentación interactiva · Tema 1 y Tema 5")

slide_index = st.session_state.slide_index
slide_title, slide_kind = SLIDES[slide_index]
previous_col, title_col, next_col = st.columns([1, 7, 1])
with previous_col:
    st.button(
        "←",
        help="Diapositiva anterior",
        on_click=_previous,
        disabled=slide_index == 0,
        width="stretch",
    )
with title_col:
    st.markdown(
        f'<div class="eyebrow">DIAPOSITIVA {slide_index + 1:02d} / {len(SLIDES):02d}</div>'
        f'<div class="slide-title">{slide_title}</div>',
        unsafe_allow_html=True,
    )
with next_col:
    st.button(
        "→",
        help="Diapositiva siguiente",
        on_click=_next,
        disabled=slide_index == len(SLIDES) - 1,
        width="stretch",
    )
st.progress((slide_index + 1) / len(SLIDES))
st.markdown("")


def input_controls(circuit_key: str, variables: list[str]) -> tuple[dict[str, int], bool]:
    st.markdown("**Entradas del circuito**")
    columns = st.columns(len(variables) + 1)
    values = {}
    for column, variable in zip(columns, variables):
        with column:
            values[variable] = st.selectbox(
                variable,
                (0, 1),
                key=f"bit_{circuit_key}_{variable}",
                format_func=lambda bit: str(bit),
            )
    with columns[-1]:
        autoplay = st.checkbox("Reproducir combinaciones", key=f"auto_{circuit_key}")
    return values, autoplay


def circuit_panel(
    circuit_key: str, circuit: dict, key: str | None = None
) -> tuple[dict[str, int], bool, int]:
    key = key or circuit_key
    values, autoplay = input_controls(key, circuit["variables"])
    result = render_circuit(circuit, values, autoplay=autoplay)
    if autoplay:
        st.caption("La salida y las señales recorren las combinaciones dentro del Canvas.")
    else:
        st.metric("Salida de la función", result)
    return values, autoplay, result


def show_truth_table(
    rows: list[dict[str, int]],
    selected_inputs: dict[str, int] | None = None,
    representation: str = "both",
    column_labels: dict[str, str] | None = None,
) -> None:
    if not rows:
        st.info("No hay filas disponibles para esta tabla.")
        return
    if representation not in {"both", "boolean", "propositional"}:
        raise ValueError(f"Representación de tabla desconocida: {representation}")

    columns = list(rows[0])
    output_columns = {"F", "Y"}
    header = "".join(
        f'<th class="{"output-head" if column in output_columns else ""}">'
        f'{escape((column_labels or {}).get(column, column))}</th>'
        for column in columns
    )
    body_rows = []
    for row in rows:
        is_active = selected_inputs is not None and all(
            row.get(name) == value for name, value in selected_inputs.items()
        )
        cells = []
        for column in columns:
            value = row[column]
            if value in (0, 1):
                truth_value = "V" if value else "F"
                truth_name = "Verdadero" if value else "Falso"
                if representation == "propositional":
                    visible_value = truth_value
                    equivalent = ""
                elif representation == "both":
                    visible_value = str(value)
                    equivalent = (
                        f'<span class="bit-equivalent" aria-label="{truth_name}">'
                        f"{truth_value}</span>"
                    )
                else:
                    visible_value = str(value)
                    equivalent = ""
                cells.append(
                    f'<td><span class="bit bit-{value}" title="{value} = {truth_name} ({truth_value})">'
                    f'<span class="bit-primary">{visible_value}</span>{equivalent}</span></td>'
                )
            else:
                cells.append(f"<td>{escape(str(value))}</td>")
        row_class = ' class="active-row"' if is_active else ""
        body_rows.append(f"<tr{row_class}>{''.join(cells)}</tr>")

    table_html = f"""
    <style>
      * {{ box-sizing:border-box; }}
      .truth-table-frame {{ color:#dce9ed; font:13px/1.35 Inter,system-ui,-apple-system,"Segoe UI",sans-serif; }}
      .table-shell {{ overflow-x:auto; border:1px solid rgba(133,177,192,.2);
        border-radius:14px; background:linear-gradient(145deg,rgba(17,37,50,.94),rgba(10,24,36,.96));
        box-shadow:0 12px 30px rgba(0,0,0,.16); margin:8px 0 12px; }}
      table {{ width:100%; border-collapse:separate; border-spacing:0; min-width:280px; }}
      th {{ position:sticky; top:0; z-index:1; padding:11px 9px; color:#a9c1ca;
        background:#142c3b; border-bottom:1px solid rgba(133,177,192,.2);
        font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }}
      th.output-head {{ color:#7ee9cc; }}
      td {{ padding:6px 8px; text-align:center; border-bottom:1px solid rgba(133,177,192,.08); }}
      tr:last-child td {{ border-bottom:0; }}
      tbody tr:nth-child(even) {{ background:rgba(110,151,167,.045); }}
      .bit {{ display:inline-flex; min-width:27px; height:27px; align-items:center;
        justify-content:center; gap:4px; padding:0 6px; border-radius:9px;
        font:700 13px ui-monospace,Consolas,monospace; }}
      .bit-equivalent {{ opacity:.78; font:700 9px ui-sans-serif,system-ui,sans-serif; }}
      .bit-1 {{ color:#83f0d2; background:rgba(54,190,157,.15); box-shadow:inset 0 0 0 1px rgba(89,229,193,.2); }}
      .bit-0 {{ color:#f0c98e; background:rgba(199,148,80,.14); box-shadow:inset 0 0 0 1px rgba(220,176,112,.17); }}
      .active-row {{ background:rgba(53,187,154,.16) !important; }}
      .active-row td {{ border-top:1px solid rgba(101,235,199,.24); border-bottom:1px solid rgba(101,235,199,.24); }}
      .active-row .bit {{ transform:scale(1.05); }}
      @keyframes rowPulse {{ 0% {{ box-shadow:inset 0 0 0 0 rgba(87,235,194,0); }}
        45% {{ box-shadow:inset 0 0 26px 0 rgba(87,235,194,.18); }}
        100% {{ box-shadow:inset 0 0 0 0 rgba(87,235,194,.05); }} }}
      .active-row {{ animation:rowPulse 1.8s ease-in-out infinite; }}
      @media (prefers-reduced-motion:reduce) {{ .active-row {{ animation:none; }} }}
    </style>
    <div class="truth-table-frame"><div class="table-shell"><table><thead><tr>{header}</tr></thead>
      <tbody>{''.join(body_rows)}</tbody></table></div></div>
    """
    st.html(table_html)
    mapping = "V corresponde a 1 y F a 0."
    active_row = (
        " La fila resaltada coincide con las entradas seleccionadas."
        if selected_inputs is not None
        else ""
    )
    st.caption(mapping + active_row)


def show_route() -> None:
    controls = st.columns([2.4, 1, 1])
    with controls[0]:
        st.selectbox(
            "Explora una estación",
            options=range(len(ROUTE_STATIONS)),
            format_func=lambda index: (
                f"{index + 1:02d} · {ROUTE_STATIONS[index]['title']}"
            ),
            key="route_step",
        )
    with controls[1]:
        st.button(
            "← Anterior",
            key="route_back",
            on_click=_move_route_back,
            disabled=st.session_state.route_step == 0,
            width="stretch",
        )
    with controls[2]:
        st.button(
            "Siguiente →",
            key="route_forward",
            on_click=_move_route_forward,
            disabled=st.session_state.route_step == len(ROUTE_STATIONS) - 1,
            width="stretch",
        )

    active_index = st.session_state.route_step
    pointer_position = (active_index + 0.5) * 100 / len(ROUTE_STATIONS)
    stations_html = "".join(
        (
            f'<div class="route-station{" active" if index == active_index else ""}">'
            f'<div class="station-index">{index + 1:02d}</div>'
            f"<strong>{escape(station['title'])}</strong>"
            f"<span>{escape(station['range'])} · {escape(station['summary'])}</span>"
            "</div>"
        )
        for index, station in enumerate(ROUTE_STATIONS)
    )
    route_illustration = """
    <svg viewBox="0 0 64 68" role="img" aria-label="Guía señalando la ruta">
      <circle cx="20" cy="12" r="8" fill="#ffc978"/>
      <path d="M12 53V39c0-9 4-15 11-15s11 6 11 15v14Z" fill="#66e5ce"/>
      <path d="M30 35 43 27h9" fill="none" stroke="#ffc978" stroke-width="6" stroke-linecap="round"/>
      <path d="M51 27h9m0 0-5-5m5 5-5 5" fill="none" stroke="#ff9e74" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="m17 53-4 9m15-9 4 9" fill="none" stroke="#a9bcff" stroke-width="5" stroke-linecap="round"/>
      <circle cx="17.5" cy="11" r="1" fill="#142339"/><circle cx="23" cy="11" r="1" fill="#142339"/>
      <path d="M18 16q3 3 6 0" fill="none" stroke="#142339" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
    """
    st.markdown(
        f"""
        <div class="route-visual">
          <div class="route-guide" style="left:{pointer_position:.1f}%">{route_illustration}</div>
          <div class="route-line"></div>
          <div class="route-stations">{stations_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    station = ROUTE_STATIONS[active_index]
    st.markdown(
        f'<div class="route-focus"><b>CONCEPTO CLAVE</b>'
        f'<span>{escape(station["concept"])}</span></div>',
        unsafe_allow_html=True,
    )


def show_gate_slide(gate: str) -> None:
    descriptions = {
        "NOT": (
            "NOT invierte el bit de entrada. Es la operación más sencilla para obtener la señal complementaria.",
            r"Y=A'",
            r"\text{Ejemplo: si }A=0,\text{ entonces }Y=1.",
        ),
        "AND": (
            "AND representa una condición conjunta: la salida solo se activa cuando todas sus entradas están en 1.",
            r"Y=A\cdot B",
            r"\text{Ejemplo: }A=1\text{ y }B=1\text{ producen }Y=1.",
        ),
        "OR": (
            "OR representa alternativas: basta con que una entrada esté en 1 para que la salida también lo esté.",
            r"Y=A+B",
            r"\text{Ejemplo: }A=1\text{ o }B=1\text{ producen }Y=1.",
        ),
    }
    description, expression, example = descriptions[gate]
    st.markdown(f'<p class="slide-lead">{description}</p>', unsafe_allow_html=True)
    st.latex(expression)
    st.latex(example)
    st.markdown("")
    left, right = st.columns([1.35, 1])
    with left:
        values, _, _ = circuit_panel(gate, CIRCUITS[gate])
    with right:
        variables = tuple(CIRCUITS[gate]["variables"])
        fn = {"NOT": lambda a: 1-a, "AND": lambda a,b: a&b, "OR": lambda a,b: a|b}[gate]
        show_truth_table(truth_table(variables, {"Y": fn}), values)


def show_exercise(exercise_key: str) -> None:
    exercise = EXERCISES[exercise_key]
    context = {
        "5.11a": "La expresión contiene términos que se reducen mediante combinación y absorción; la tabla de verdad verifica la equivalencia.",
        "5.11b": "De Morgan transforma el primer término y la distribución desarrolla el segundo en forma suma de productos, verificable para las ocho combinaciones.",
        "5.12": "La función se implementa únicamente con compuertas NAND a partir de su forma suma de productos.",
        "5.13": "El producto de sumas se implementa únicamente con NOR mediante De Morgan y la negación doble.",
    }
    st.markdown(f'<p class="slide-lead">{context[exercise_key]}</p>', unsafe_allow_html=True)
    st.latex(exercise["expression"])
    if exercise_key == "5.11a":
        values, autoplay = input_controls(
            "511a-comparison", CIRCUITS["5.11a"]["variables"]
        )
        left, right = st.columns([1, 1.15], gap="large")
        with left:
            st.markdown("#### Resolución")
            for title, step in exercise["steps"]:
                st.markdown(f"**{title}**")
                st.latex(step)
        with right:
            st.markdown("#### Tabla de verdad")
            show_truth_table(exercise_tables()[exercise_key], values)
        original_col, simple_col = st.columns(2, gap="medium")
        with original_col:
            st.markdown("#### Circuito original")
            original = render_circuit(CIRCUITS["5.11a"], values, autoplay=autoplay)
            if autoplay:
                st.caption("F recorre combinaciones")
            else:
                st.metric("F original", original)
        with simple_col:
            st.markdown("#### Circuito simplificado")
            simplified = render_circuit(CIRCUITS["5.11a-simplified"], values, autoplay=autoplay)
            if autoplay:
                st.caption("F recorre combinaciones")
            else:
                st.metric("F simplificada", simplified)
        return
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        st.markdown("#### Resolución")
        for title, step in exercise["steps"]:
            st.markdown(f"**{title}**")
            st.latex(step)
        values, _, _ = circuit_panel(exercise_key, CIRCUITS[exercise_key])
    with right:
        st.markdown("#### Tabla de verdad")
        show_truth_table(exercise_tables()[exercise_key], values)
        if exercise_key == "5.12":
            st.markdown("**Conteo:** seis NAND, incluidas las dos inversiones construidas con entradas unidas.")
        elif exercise_key == "5.13":
            st.markdown("**Conteo:** cinco NOR, incluidas las dos inversiones construidas con entradas unidas.")
        elif exercise_key == "5.11b":
            st.markdown("La tabla comprueba que la forma desarrollada mantiene la salida para las ocho combinaciones posibles.")


if slide_kind == "cover":
    campus_uri = image_data_uri(find_visual_asset("campus"))
    logo_uri = image_data_uri(find_visual_asset("school_logo"))
    boole_uri = image_data_uri(find_visual_asset("boole_guide"))
    campus_style = f"background-image:url('{campus_uri}');" if campus_uri else ""
    logo_markup = (
        f'<img class="school-logo" src="{logo_uri}" alt="Logo de la Escuela de Estadística e Informática">'
        if logo_uri
        else '<div class="logo-fallback" aria-label="Escuela de Estadística e Informática">EI</div>'
    )
    boole_markup = (
        f'<img class="boole-portrait" src="{boole_uri}" alt="Retrato de George Boole">'
        if boole_uri
        else '<div class="boole-placeholder" aria-hidden="true">⌘</div>'
    )
    st.markdown(
        f"""
        <section class="cover-hero">
          <div class="cover-backdrop" style="{campus_style}"></div>
          <div class="cover-shade"></div>
          <div class="cover-content">
            <div class="eyebrow">PRESENTACIÓN INTERACTIVA · SISTEMAS DIGITALES</div>
            <div class="hero-title">Compuertas<br><span>lógicas</span> &amp;<br>Álgebra de Boole</div>
            <p class="hero-sub">De los bits a los circuitos: cómo una computadora toma decisiones con señales binarias.</p>
            <p class="cover-context">En la universidad estudiamos estas reglas porque están detrás de la electrónica digital y de las decisiones que ejecutan los sistemas. Las compuertas procesan señales; el Álgebra de Boole nos ayuda a describirlas, comprobarlas y diseñar circuitos equivalentes.</p>
            <div class="group-heading"><span class="group-mark">®✓</span><strong>GRUPO ®✓ · Sistemas digitales</strong></div>
          </div>
          <aside class="cover-side">
            {logo_markup}
            <div class="boole-card">{boole_markup}<div><strong>George Boole</strong><span>Una idea lógica, muchas aplicaciones digitales</span></div></div>
          </aside>
        </section>
        """,
        unsafe_allow_html=True,
    )
    members = [
        "CHAGARAY LOZA ADRIANO",
        "VILLAFUERTE VELASQUEZ SNAIDER",
        "HENRRIQUEZ BEJAR ANGELO",
        "ANGELES CARLOS DEZA",
        "quispe lucas cristian david",
        "rivas chiroque milagros alexandra",
    ]
    member_cards = "".join(
        f'<div class="member-card">{escape(member)}</div>' for member in members
    )
    st.markdown(
        '<div class="group-heading"><span class="group-mark">6</span><strong>Integrantes</strong></div>'
        f'<div class="members-grid">{member_cards}</div>',
        unsafe_allow_html=True,
    )
    st.caption("Navegación por flechas o selector lateral; ajusta las entradas para explorar cada circuito.")

elif slide_kind == "index":
    st.markdown(
        '<p class="slide-lead">Elige una estación o avanza con las flechas. La guía señala el tramo actual; cada tarjeta resume la idea que conecta con la siguiente.</p>',
        unsafe_allow_html=True,
    )
    show_route()

elif slide_kind == "definition":
    st.markdown(
        '<p class="slide-lead">Una compuerta lógica recibe una o más señales binarias, aplica una operación definida y entrega otra señal binaria.</p>',
        unsafe_allow_html=True,
    )
    st.latex(r"\mathrm{Entradas}\ (0\ \mathrm{o}\ 1)\longrightarrow\mathrm{operacion\ logica}\longrightarrow\mathrm{salida}\ (0\ \mathrm{o}\ 1)")
    st.markdown(
        '<div class="concept-panel">En un circuito físico, 0 y 1 representan rangos de voltaje que el sistema interpreta como estados distintos. '
        'La regla de cada compuerta determina la salida para cada combinación de entradas; una expresión o tabla de verdad permite comprobarla.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("#### Ejemplo: una condición conjunta")
    st.markdown("La compuerta AND se activa solo cuando las dos señales de entrada están activas.")
    circuit_panel("definition-and", CIRCUITS["AND"])

elif slide_kind == "algebra":
    st.markdown(
        '<p class="slide-lead">El Álgebra de Boole describe relaciones entre señales que solo pueden tomar los valores 0 y 1. '
        'Sus operaciones básicas son complemento, producto y suma.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("#### Valores de verdad y señales digitales")
    st.markdown(
        "Una proposición lógica es verdadera o falsa. Al asociar las proposiciones "
        "p y q con las señales A y B, sus tablas de verdad representan los mismos casos."
    )
    st.latex(r"\mathrm{Verdadero}\ (V)\leftrightarrow1,\qquad \mathrm{Falso}\ (F)\leftrightarrow0")
    st.latex(
        r"\neg p\leftrightarrow A',\qquad "
        r"p\land q\leftrightarrow A\cdot B,\qquad "
        r"p\lor q\leftrightarrow A+B"
    )
    st.caption(
        "Negación = NOT; conjunción (y) = AND; disyunción inclusiva (o) = OR."
    )
    with st.expander("Condicional lógico"):
        st.latex(r"p\to q\equiv\neg p\lor q,\qquad A\to B\equiv A'+B")
        st.write(
            "La implicación es falsa únicamente cuando la primera proposición es verdadera y la segunda es falsa."
        )

    operation_notes = {
        "NOT": ("El complemento invierte cada estado binario: convierte el 0 en 1 y el 1 en 0.", r"A'"),
        "AND": ("El producto lógico exige que ambas condiciones se cumplan para que el resultado sea 1.", r"A\cdot B"),
        "OR": ("La suma lógica es inclusiva: el resultado es 1 si una o ambas entradas valen 1.", r"A+B"),
    }
    algebra_gate = st.selectbox("Explora una operación", ("NOT", "AND", "OR"), key="algebra_gate")
    note, formula = operation_notes[algebra_gate]
    st.markdown(note)
    st.latex(formula)
    values, _, _ = circuit_panel(f"algebra-{algebra_gate}", CIRCUITS[algebra_gate])
    fn = {
        "NOT": lambda a: 1-a,
        "AND": lambda a, b: a & b,
        "OR": lambda a, b: a | b,
    }[algebra_gate]
    representation_label = st.selectbox(
        "Representación de valores en la tabla",
        ("Ambas: 1/V y 0/F", "Booleana: 1/0", "Proposicional: V/F"),
        key="algebra_truth_view",
    )
    representation = {
        "Ambas: 1/V y 0/F": "both",
        "Booleana: 1/0": "boolean",
        "Proposicional: V/F": "propositional",
    }[representation_label]
    propositional_headers = {
        "NOT": {"A": "p", "Y": "¬p"},
        "AND": {"A": "p", "B": "q", "Y": "p ∧ q"},
        "OR": {"A": "p", "B": "q", "Y": "p ∨ q"},
    }
    show_truth_table(
        truth_table(tuple(CIRCUITS[algebra_gate]["variables"]), {"Y": fn}),
        values,
        representation,
        propositional_headers[algebra_gate]
        if representation == "propositional"
        else None,
    )

elif slide_kind in ("NOT", "AND", "OR"):
    show_gate_slide(slide_kind)

elif slide_kind == "derived":
    st.markdown(
        '<p class="slide-lead">Las compuertas derivadas amplían las posibilidades: NAND y NOR invierten el resultado de AND y OR; '
        'XOR y XNOR comparan si dos señales son distintas o iguales.</p>',
        unsafe_allow_html=True,
    )
    st.latex(r"\operatorname{NAND}(A,B)=(A\cdot B)',\quad \operatorname{NOR}(A,B)=(A+B)'")
    st.latex(r"A\oplus B=1\ \text{si }A\ne B,\qquad \operatorname{XNOR}(A,B)=1\ \text{si }A=B")
    st.markdown(
        "NAND y NOR se llaman universales porque, combinadas adecuadamente, permiten implementar NOT, AND y OR y, por tanto, "
        "cualquier función booleana. Esta propiedad permite implementar funciones complejas con una sola familia de compuertas."
    )
    gate = st.selectbox("Prueba una compuerta", ("NAND", "NOR", "XOR", "XNOR"), key="derived_gate")
    descriptions = {
        "NAND": r"Y=(A\cdot B)'",
        "NOR": r"Y=(A+B)'",
        "XOR": r"Y=A\oplus B",
        "XNOR": r"Y=(A\oplus B)'",
    }
    st.latex(descriptions[gate])
    values, _, _ = circuit_panel(f"derived-{gate}", CIRCUITS[gate])
    gate_function = {
        "NAND": lambda a, b: 1 - (a & b),
        "NOR": lambda a, b: 1 - (a | b),
        "XOR": lambda a, b: a ^ b,
        "XNOR": lambda a, b: int(a == b),
    }[gate]
    show_truth_table(truth_table(("A", "B"), {"Y": gate_function}), values)

elif slide_kind == "laws":
    st.markdown(
        '<p class="slide-lead">Las leyes booleanas son equivalencias: cada término puede sustituirse por una forma equivalente '
        'sin cambiar el resultado para ninguna combinación de entradas.</p>',
        unsafe_allow_html=True,
    )
    law_columns = st.columns(2)
    for index, (name, formula, explanation) in enumerate(LAWS):
        with law_columns[index % 2]:
            with st.container(border=True):
                st.markdown(f"**{name}**")
                st.latex(formula)
                st.write(explanation)
    st.markdown("### De Morgan: cambiar la operación al negar")
    st.markdown(
        "Las dos leyes muestran que negar una expresión completa equivale a negar cada entrada y cambiar la operación. "
        "No es una regla para quitar una marca de complemento sin más: hay que complementar los términos y cambiar AND por OR "
        "o OR por AND."
    )
    de_morgan_left, de_morgan_right = st.columns(2)
    with de_morgan_left:
        st.markdown("**Negación de una conjunción**")
        st.latex(r"(A\cdot B)'=A'+B'")
        st.latex(r"\neg(p\land q)\equiv\neg p\lor\neg q")
        st.markdown(
            "La negación de AND equivale a una OR de complementos; NAND integra la conjunción y su negación."
        )
    with de_morgan_right:
        st.markdown("**Negación de una disyunción**")
        st.latex(r"(A+B)'=A'\cdot B'")
        st.latex(r"\neg(p\lor q)\equiv\neg p\land\neg q")
        st.markdown(
            "La negación de OR equivale a una AND de complementos; NOR integra la disyunción y su negación."
        )
    st.markdown(
        '<div class="concept-panel">NAND y NOR incorporan una negación en la salida. Las Leyes de De Morgan permiten reorganizar la expresión '
        'para aprovechar esa negación y reducir compuertas adicionales, como se muestra en los ejercicios 5.12 y 5.13.</div>',
        unsafe_allow_html=True,
    )

elif slide_kind in ("5.11a", "5.11b", "5.12", "5.13"):
    show_exercise(slide_kind)

elif slide_kind == "references":
    st.markdown(
        '<p class="slide-lead">Los materiales de <code>libros/</code> permiten contrastar la notación y las consignas del curso. '
        'La aplicación funciona aunque esa carpeta esté vacía.</p>',
        unsafe_allow_html=True,
    )
    st.info(
        "Referencia al ejercicio 5.14: el enunciado no está incluido entre los materiales disponibles en este proyecto. "
        "Su resolución requiere consultar la guía o el libro oficial del curso."
    )
    st.markdown(
        "La vista previa permite localizar contenido extraído; la notación y las indicaciones oficiales del material siguen siendo la referencia."
    )
    references = list_references()
    if not references:
        st.info("No se encontraron PDF, PPTX, TXT o MD en libros/ ni en libros-materiales-de-referencia/. La presentación funciona sin ellos.")
    else:
        st.markdown("#### Archivos detectados")
        for path in references:
            st.markdown(f"- `{path}`")
        selected = st.selectbox(
            "Selecciona un documento para extraer una vista previa",
            references,
            format_func=lambda path: path.name,
            key="reference_selection",
        )
        if st.button("Leer vista previa", key="read_reference"):
            try:
                st.session_state.reference_text = read_reference(selected)
                st.session_state.reference_error = ""
            except (OSError, RuntimeError, ValueError) as error:
                st.session_state.reference_error = str(error)
        if st.session_state.get("reference_error"):
            st.error(st.session_state.reference_error)
        if st.session_state.get("reference_text"):
            st.text_area("Texto extraído", st.session_state.reference_text, height=280)

elif slide_kind == "closing":
    st.markdown('<div class="hero-title">De una expresión<br>a un circuito.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Las tablas de verdad verifican el comportamiento; las leyes de Boole ayudan '
        'a encontrar una implementación equivalente y más clara.</p>',
        unsafe_allow_html=True,
    )
    takeaway_columns = st.columns(3)
    takeaways = [
        ("Señales", "La salida queda determinada por los valores de entrada y la función de la compuerta."),
        ("Equivalencia", "La expresión, la tabla y el circuito representan la misma función; simplificar no debe alterar ninguna fila."),
        ("Implementación", "Las leyes, especialmente De Morgan, permiten convertir funciones a redes de compuertas NAND o NOR."),
    ]
    for column, (title, text) in zip(takeaway_columns, takeaways):
        with column:
            st.markdown(
                f'<div class="info-card"><strong>{title}</strong><br><br>{text}</div>',
                unsafe_allow_html=True,
            )
    st.markdown("")
    st.markdown(
        '<div class="concept-panel">Una función se describe mediante su expresión booleana, su tabla de verdad y su circuito. '
        'La equivalencia entre estas representaciones verifica que el circuito implementa la función deseada.</div>',
        unsafe_allow_html=True,
    )
    st.caption("GRUPO ®✓ · Compuertas lógicas y Álgebra de Boole")
