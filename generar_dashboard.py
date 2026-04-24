import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. CARGA Y LIMPIEZA DE DATOS
# ---------------------------------------------------------
print("Cargando datos...")
df = pd.read_csv('co-emissions-per-capita.csv')

# Renombrar columnas para facilitar el trabajo
df.rename(columns={
    'Entity': 'Pais', 
    'Code': 'Codigo', 
    'Year': 'Año', 
    'CO₂ emissions per capita': 'CO2_per_capita'
}, inplace=True)

# Limpiar datos: Quitar valores nulos y agrupaciones mundiales/regionales
# Los países reales suelen tener un código de 3 letras. Los grupos de "Our World in Data" empiezan por OWID
df = df.dropna(subset=['Codigo'])
df = df[~df['Codigo'].str.startswith('OWID')]

año_reciente = df['Año'].max()
df_reciente = df[df['Año'] == año_reciente]

# ---------------------------------------------------------
# 2. GRÁFICA 1: EL RANKING DE "VILLANOS" (TOP 15)
# ---------------------------------------------------------
print("Generando Gráfica 1...")
top_15 = df_reciente.sort_values(by='CO2_per_capita', ascending=False).head(15)

# Configurar estilo visual moderno (oscuro, ideal para jóvenes)
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))

# Crear barras
sns.barplot(
    data=top_15, 
    x='CO2_per_capita', 
    y='Pais', 
    palette='Reds_r' # Degradado rojo para indicar alarma
)

plt.title(f'🚨 Los 15 países con mayor huella de carbono por persona ({año_reciente})', fontsize=16, fontweight='bold', pad=20, color='white')
plt.xlabel('Toneladas de CO2 producidas por cada habitante al año', fontsize=12, color='lightgray')
plt.ylabel('', fontsize=12)

# Añadir los números al final de cada barra para no tener que adivinar
for index, value in enumerate(top_15['CO2_per_capita']):
    plt.text(value, index, f' {value:.1f} t', color='white', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('01_ranking_top15.png', dpi=300, transparent=True)
plt.close()

# ---------------------------------------------------------
# 3. GRÁFICA 2: MÁQUINA DEL TIEMPO (Evolución)
# ---------------------------------------------------------
print("Generando Gráfica 2...")
# Tomar el país #1 del top y un par de países conocidos para comparar
pais_top = top_15.iloc[0]['Pais']
paises_comparar = [pais_top, 'United States', 'Colombia', 'China'] 
df_linea = df[df['Pais'].isin(paises_comparar)]

plt.figure(figsize=(10, 6))
sns.lineplot(
    data=df_linea, 
    x='Año', 
    y='CO2_per_capita', 
    hue='Pais', 
    linewidth=3,
    palette='Set1'
)

# Resaltar la fecha aproximada de nacimiento de un joven de 15 años hoy (aprox 2009)
plt.axvline(x=2009, color='cyan', linestyle='--', linewidth=2)
plt.text(2010, df_linea['CO2_per_capita'].max() * 0.8, '← ¡Aquí naciste tú!', color='cyan', fontsize=12, fontweight='bold')

plt.title('⏳ ¿Cómo ha cambiado el mundo desde que naciste?', fontsize=16, fontweight='bold', pad=20, color='white')
plt.xlabel('Año', fontsize=12, color='lightgray')
plt.ylabel('Toneladas de CO2 por persona', fontsize=12, color='lightgray')
plt.legend(title='País', facecolor='#222222', edgecolor='white', labelcolor='white')

plt.tight_layout()
plt.savefig('02_evolucion_historica.png', dpi=300, transparent=True)
plt.close()

# ---------------------------------------------------------
# 4. NARRATIVA DE IMPACTO (Para copiar a Power BI)
# ---------------------------------------------------------
print("\n" + "="*50)
print("✅ IMÁGENES GENERADAS CON ÉXITO")
print("Busca los archivos '01_ranking_top15.png' y '02_evolucion_historica.png' en esta carpeta.")
print("="*50 + "\n")

# Cálculos de narrativa para el peor país
peor_emisor = top_15.iloc[0]['Pais']
peor_emision = top_15.iloc[0]['CO2_per_capita']

# Equivalencias (Aprox)
smartphones_por_tonelada = 121000
arboles_por_tonelada = 50

smartphones_total = int(peor_emision * smartphones_por_tonelada)
arboles_total = int(peor_emision * arboles_por_tonelada)

print("📝 TEXTO PARA COPIAR EN LOS CUADROS DE TEXTO DE POWER BI:")
print("-" * 50)
print("TÍTULO O TARJETA 1:")
print(f"¿Sabías que una persona promedio en {peor_emisor} produce {peor_emision:.1f} toneladas de CO2 al año?")
print("\nTARJETA DE IMPACTO 2 (El Celular):")
print(f"📱 Eso equivale a cargar un smartphone {smartphones_total:,} veces. ¡Es como cargar tu celular todos los días durante {(smartphones_total/365):.0f} años!")
print("\nTARJETA DE IMPACTO 3 (Los Árboles):")
print(f"🌳 Para limpiar la contaminación de UNA SOLA PERSONA en ese país, necesitaríamos plantar un mini-bosque de {arboles_total} árboles cada año.")
print("-" * 50)