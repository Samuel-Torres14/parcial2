/**
 * Universidad - Facultad de Ingeniería
 * Asignatura: Introducción a la Computación Gráfica
 * Tarea: Rasterización manual (Bresenham + Punto Medio)
 */

//  funcion para PIXEL 
function drawPixel(ctx, x, y, color = "#000") {
    ctx.fillStyle = color;
    ctx.fillRect(Math.floor(x), Math.floor(y), 1, 1);
}

// la funcion Bresenham
function bresenhamLine(ctx, x0, y0, x1, y1, color = "#000") {

    x0 = Math.floor(x0);
    y0 = Math.floor(y0);
    x1 = Math.floor(x1);
    y1 = Math.floor(y1);

    let dx = Math.abs(x1 - x0);
    let dy = Math.abs(y1 - y0);

    let sx = (x0 < x1) ? 1 : -1;
    let sy = (y0 < y1) ? 1 : -1;

    let err = dx - dy;

    while (true) {
        drawPixel(ctx, x0, y0, color);

        if (x0 === x1 && y0 === y1) break;

        let e2 = 2 * err;

        /**Lógica del error:
         * e2 evalúa si debemos movernos en X, Y o ambos.
         * Permite manejar todos los octantes (m > 1, m < 0, etc).*/

        if (e2 > -dy) {
            err -= dy;
            x0 += sx;
        }

        if (e2 < dx) {
            err += dx;
            y0 += sy;
        }
    }
}

// funcion para circunferencia
function midpointCircle(ctx, xc, yc, r, color = "#000") {

    let x = 0;
    let y = r;

    let p = 1 - r;

    while (x <= y) {

        // Simetría de 8 octantes
        drawPixel(ctx, xc + x, yc + y, color);
        drawPixel(ctx, xc - x, yc + y, color);
        drawPixel(ctx, xc + x, yc - y, color);
        drawPixel(ctx, xc - x, yc - y, color);
        drawPixel(ctx, xc + y, yc + x, color);
        drawPixel(ctx, xc - y, yc + x, color);
        drawPixel(ctx, xc + y, yc - x, color);
        drawPixel(ctx, xc - y, yc - x, color);

        x++;

         /**Parámetro de decisión:
         * p < 0 : el punto está dentro y solo avanzamos en x
         * p >= 0 : el punto está fuera y decrementamos  y */

        if (p < 0) {
            p = p + 2 * x + 1;
        } else {
            y--;
            p = p + 2 * (x - y) + 1;
        }
    }
}
// funcion para poligono (segun el ejemplo)
function getPolygonVertices(cx, cy, sides, radius) {

    let vertices = [];

    for (let i = 0; i < sides; i++) {

        let angle = (2 * Math.PI * i) / sides;

        let x = cx + radius * Math.cos(angle);
        let y = cy + radius * Math.sin(angle);

        vertices.push({ x, y });
    }

    return vertices;
}
// parte del main para inicializar todo en conjunto 
window.onload = function () {

    // obtiene el canvas y su contexto 2D para dibujar
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // calcula el centro del canvas (punto de referencia geometrico)
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // genera un numero aleatorio de lados entre 5 y 10
    const sides = Math.floor(Math.random() * 6) + 5;

    // define el radio del poligono
    const R = 150;

    // calcula los vertices del poligono usando trigonometria
    const vertices = getPolygonVertices(centerX, centerY, sides, R);

    /**dibujo del poligono:
     * Se conectan los vertices consecutivos mediante el algoritmo de Bresenham.
     * El uso de (i + 1) % n permite cerrar la figura uniendo el último vértice con el primero.
     */
    for (let i = 0; i < vertices.length; i++) {
        let p1 = vertices[i];
        let p2 = vertices[(i + 1) % vertices.length];

        bresenhamLine(ctx, p1.x, p1.y, p2.x, p2.y);
    }

    /**Dibujo de circunferencias en cada vertice:
     * Para cada punto del poligono se traza una circunferencia
     * usando el algoritmo de punto medio, con radio R/4.
     */
    vertices.forEach(v => {
        midpointCircle(ctx, v.x, v.y, R / 4);
    });

};
