import math
import random
from pathlib import Path
from html import escape


# ============================================================
# CONFIGURACIÓN
# ============================================================

WIDTH = 107
HEIGHT = 14

CELL_W = 9
CELL_H = 18

SVG_WIDTH = WIDTH * CELL_W
SVG_HEIGHT = HEIGHT * CELL_H

OUTPUT = Path("assets/tree.svg")


# ============================================================
# ÁRBOL
# ============================================================

TREE = r"""       ***        **  **  ***
     ******     ****** ********
    ***\/****  **\/**\/__/***
   **\  \   |  |  \__// **\*****
  ***/\_ \________/~_/   ***** |
******* \/~-_______/  **  **   |
|  **\__//~/____   \__/***
|  **/* \_____ ~\_   *\*******
|   ****      \_\~\  ******  |
      |        ////    * |   |
      |       ////       |
             /~~~\ """


TREE_LINES = TREE.splitlines()

TREE_W = max(
    len(line)
    for line in TREE_LINES
)

TREE_H = len(TREE_LINES)

# Centrado dentro de las 107 columnas
TREE_X = (WIDTH - TREE_W) // 2

TREE_Y = 1


# ============================================================
# COLORES
# ============================================================

# Hojas
BLUE = "#00afff"

# Lianas / partículas
CYAN = "#00d7ff"

# Madera
BROWN = "#875f00"

# Madera clara
LIGHT_BROWN = "#af8700"


# ============================================================
# ESCAPAR CARACTERES PARA SVG
# ============================================================

def svg_char(char):
    return escape(char)


# ============================================================
# POSICIONES DE LAS HOJAS REALES
# ============================================================

LEAF_POSITIONS = []

for y, line in enumerate(TREE_LINES):

    for x, char in enumerate(line):

        if char == "*":

            LEAF_POSITIONS.append(
                (
                    TREE_X + x,
                    TREE_Y + y
                )
            )


# ============================================================
# CELDAS OCUPADAS POR EL ÁRBOL
# ============================================================

TREE_CELLS = set()

for y, line in enumerate(TREE_LINES):

    for x, char in enumerate(line):

        if char != " ":

            TREE_CELLS.add(
                (
                    TREE_X + x,
                    TREE_Y + y
                )
            )


# ============================================================
# COLOR SEGÚN CARÁCTER
# ============================================================

def get_color(char):

    # Hojas
    if char == "*":
        return BLUE

    # Lianas
    if char == "|":
        return CYAN

    # Madera
    if char in "/\\_-":
        return BROWN

    # Madera clara
    if char == "~":
        return LIGHT_BROWN

    return None


# ============================================================
# GENERAR ÁRBOL
# ============================================================

def generate_tree():

    elements = []

    for y, line in enumerate(TREE_LINES):

        for x, char in enumerate(line):

            if char == " ":
                continue

            color = get_color(char)

            if color is None:
                continue

            px = (
                TREE_X + x
            ) * CELL_W

            py = (
                TREE_Y + y + 1
            ) * CELL_H

            elements.append(
                f'''
<text
    x="{px}"
    y="{py}"
    fill="{color}"
>{svg_char(char)}</text>'''
            )

    return "\n".join(elements)


# ============================================================
# GENERAR HOJA VOLADORA
# ============================================================

def generate_leaf(index):

    # --------------------------------------------------------
    # POSICIÓN INICIAL
    # --------------------------------------------------------

    start_x, start_y = random.choice(
        LEAF_POSITIONS
    )

    # --------------------------------------------------------
    # DIRECCIÓN
    #
    # 75% derecha
    # 25% izquierda
    # --------------------------------------------------------

    direction = random.choice([
        1,
        1,
        1,
        -1
    ])

    # --------------------------------------------------------
    # DISTANCIA HORIZONTAL
    # --------------------------------------------------------

    horizontal_distance = random.uniform(
        7,
        17
    ) * direction

    # --------------------------------------------------------
    # DISTANCIA VERTICAL
    #
    # IMPORTANTE:
    # se calcula UNA sola vez por hoja.
    # --------------------------------------------------------

    vertical_distance = random.uniform(
        5,
        8
    )

    # --------------------------------------------------------
    # PUNTOS DE LA TRAYECTORIA
    # --------------------------------------------------------

    steps = random.randint(
        6,
        9
    )

    positions_x = []
    positions_y = []

    # --------------------------------------------------------
    # ONDULACIÓN
    # --------------------------------------------------------

    phase = random.uniform(
        0,
        math.tau
    )

    wave_amount = random.uniform(
        0.5,
        1.4
    )

    # --------------------------------------------------------
    # GENERAR TRAYECTORIA
    # --------------------------------------------------------

    for step in range(steps):

        progress = (
            step
            / (steps - 1)
        )

        # Movimiento horizontal
        x = (
            start_x
            + horizontal_distance
            * progress
        )

        # Serpenteo por viento
        x += (
            math.sin(
                progress
                * math.tau
                * 1.5
                + phase
            )
            * wave_amount
        )

        # Caída vertical consistente
        y = (
            start_y
            + vertical_distance
            * progress
        )

        positions_x.append(
            x * CELL_W
        )

        positions_y.append(
            (y + 1) * CELL_H
        )

    # --------------------------------------------------------
    # LIMITAR POSICIONES AL SVG
    # --------------------------------------------------------

    positions_x = [

        max(
            0,
            min(
                SVG_WIDTH,
                value
            )
        )

        for value in positions_x
    ]

    positions_y = [

        max(
            0,
            min(
                SVG_HEIGHT,
                value
            )
        )

        for value in positions_y
    ]

    # --------------------------------------------------------
    # CONVERTIR POSICIONES A SVG
    # --------------------------------------------------------

    xs = ";".join(
        f"{value:.1f}"
        for value in positions_x
    )

    ys = ";".join(
        f"{value:.1f}"
        for value in positions_y
    )

    # --------------------------------------------------------
    # VELOCIDAD
    #
    # La dejamos igual porque esta versión ya te gustó.
    # --------------------------------------------------------

    duration = random.uniform(
        3.5,
        6.5
    )

    # --------------------------------------------------------
    # DELAY
    #
    # Evita que todas salgan al mismo tiempo.
    # --------------------------------------------------------

    delay = random.uniform(
        0,
        6
    )

    # --------------------------------------------------------
    # CARÁCTER
    # --------------------------------------------------------

    char = random.choice([
        "*",
        "*",
        "*",
        "✦",
        "·"
    ])

    # --------------------------------------------------------
    # SVG DE LA HOJA
    # --------------------------------------------------------

    return f'''
<text
    x="0"
    y="0"
    fill="{CYAN}"
    opacity="0"
>
    {svg_char(char)}

    <animate
        attributeName="x"
        values="{xs}"
        dur="{duration:.2f}s"
        begin="{delay:.2f}s"
        repeatCount="indefinite"
    />

    <animate
        attributeName="y"
        values="{ys}"
        dur="{duration:.2f}s"
        begin="{delay:.2f}s"
        repeatCount="indefinite"
    />

    <animate
        attributeName="opacity"
        values="0;1;1;1;0"
        keyTimes="0;0.08;0.60;0.85;1"
        dur="{duration:.2f}s"
        begin="{delay:.2f}s"
        repeatCount="indefinite"
    />

</text>
'''


# ============================================================
# GENERAR SVG COMPLETO
# ============================================================

def generate_svg():

    tree = generate_tree()

    # 8 hojas voladoras
    leaves = "\n".join(
        generate_leaf(i)
        for i in range(8)
    )

    return f'''<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{SVG_WIDTH}"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
>

<style>

text {{
    font-family:
        "Cascadia Mono",
        "JetBrains Mono",
        "Consolas",
        monospace;

    font-size: 16px;
    font-weight: bold;

    white-space: pre;
}}

</style>


<!-- ====================================================== -->
<!-- HOJAS VOLANDO                                           -->
<!--                                                        -->
<!-- Se dibujan PRIMERO para quedar DETRÁS del árbol.       -->
<!-- ====================================================== -->

<g id="falling-leaves">

{leaves}

</g>


<!-- ====================================================== -->
<!-- ÁRBOL                                                  -->
<!--                                                        -->
<!-- Se dibuja DESPUÉS para quedar ENCIMA de las hojas.     -->
<!-- ====================================================== -->

<g id="tree">

{tree}

</g>


</svg>
'''


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # CREAR assets/ SI NO EXISTE
    # --------------------------------------------------------

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # GENERAR
    # --------------------------------------------------------

    svg = generate_svg()

    # --------------------------------------------------------
    # GUARDAR
    # --------------------------------------------------------

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print(
        f"Generated: {OUTPUT}"
    )

    print(
        f"Grid: {WIDTH}x{HEIGHT}"
    )

    print(
        f"SVG: {SVG_WIDTH}x{SVG_HEIGHT}px"
    )

    print()


# ============================================================
# GO
# ============================================================

if __name__ == "__main__":
    main()