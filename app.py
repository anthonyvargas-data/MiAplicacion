import streamlit as st
import pandas as pd
import numpy as np

# Módulos locales
from libreria_funciones_proyecto1 import calcular_metricas_clasificacion
from libreria_clases_proyecto1 import InventarioProducto

# Configuración base
st.set_page_config(page_title="Proyecto Python - A. Vargas", layout="wide")

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox(
    "Ir a:",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)

# ==========================================
# HOME
# ==========================================
if opcion == "Home":
    st.title("Especialización en Python for Analytics")
    st.subheader("Módulo 1: Python Fundamentals")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Perfil
        * **Estudiante:** Anthony Vargas Aquino
        * **Año:** 2026
        * **Módulo:** 1 - Python Fundamentals
        
        ### Sobre el proyecto
        Esta app es el consolidado práctico del módulo. Incluye el manejo de flujos de caja, 
        estructuración de datos con NumPy/Pandas, evaluación de modelos de clasificación y 
        un CRUD de inventario usando POO.
        
        ### Stack
        - Python 3
        - Streamlit
        - NumPy & Pandas
        """)
        
    with col2:
        try:
            st.image("logo_dmc.png", use_container_width=True)
        except:
            pass # Falla silenciosa si no hay logo, no hace falta alertar al usuario final

# ==========================================
# EJERCICIO 1: FLUJO DE CAJA
# ==========================================
elif opcion == "Ejercicio 1":
    st.header("Flujo de Caja")
    st.write("Registro de ingresos y gastos.")
    st.markdown("---")
    
    # Init state
    if 'movimientos' not in st.session_state:
        st.session_state.movimientos = []
        
    c1, c2, c3 = st.columns(3)
    
    with c1:
        concepto = st.text_input("Concepto:")
    with c2:
        tipo_mov = st.selectbox("Tipo:", ["Ingreso", "Gasto"])
    with c3:
        valor = st.number_input("Monto:", min_value=0.0, step=10.0)
        
    if st.button("Registrar"):
        if not concepto.strip() or valor <= 0:
            st.warning("Verifica los datos ingresados.")
        else:
            st.session_state.movimientos.append({
                "Concepto": concepto,
                "Tipo": tipo_mov,
                "Valor": valor
            })
            st.success("Registrado.")

    st.markdown("---")

    # Resultados
    if st.session_state.movimientos:
        st.subheader("Detalle de movimientos")
        df_movs = pd.DataFrame(st.session_state.movimientos)
        st.dataframe(df_movs, use_container_width=True)
        
        # KPIs
        ingresos = df_movs[df_movs['Tipo'] == 'Ingreso']['Valor'].sum()
        gastos = df_movs[df_movs['Tipo'] == 'Gasto']['Valor'].sum()
        saldo = ingresos - gastos
        
        st.write("### Resumen")
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Ingresos", f"${ingresos:,.2f}")
        kpi2.metric("Gastos", f"${gastos:,.2f}")
        kpi3.metric("Saldo", f"${saldo:,.2f}")
        
        if saldo >= 0:
            st.info("Estado: A favor")
        else:
            st.error("Estado: En contra")

# ==========================================
# EJERCICIO 2: NUMPY & PANDAS
# ==========================================
elif opcion == "Ejercicio 2":
    st.header("Registro de Productos")
    st.markdown("---")
    
    if 'data_numpy' not in st.session_state:
        st.session_state.data_numpy = []
        
    c1, c2 = st.columns(2)
    with c1:
        nombre = st.text_input("Producto:")
        cat = st.selectbox("Categoría:", ["Tecnología", "Oficina", "Hogar", "Otros"])
    with c2:
        precio = st.number_input("Precio:", min_value=0.0, step=1.5)
        cant = st.number_input("Cantidad:", min_value=1, step=1)
        
    if st.button("Agregar"):
        if not nombre.strip():
            st.warning("Falta el nombre del producto.")
        else:
            total = precio * cant
            # Guardamos como array
            row_array = np.array([nombre, cat, precio, cant, total])
            st.session_state.data_numpy.append(row_array)
            st.success("Agregado.")
            
    st.markdown("---")
    
    # Vista de DataFrame
    if st.session_state.data_numpy:
        st.subheader("Base de Datos")
        matriz = np.array(st.session_state.data_numpy)
        
        df_prod = pd.DataFrame(matriz, columns=["Producto", "Categoría", "Precio", "Cantidad", "Total"])
        
        # Casteo de tipos para poder operar luego
        df_prod[["Precio", "Cantidad", "Total"]] = df_prod[["Precio", "Cantidad", "Total"]].apply(pd.to_numeric)
        
        st.dataframe(df_prod, use_container_width=True)

# ==========================================
# EJERCICIO 3: FUNCIONES (Métricas ML)
# ==========================================
elif opcion == "Ejercicio 3":
    st.header("Evaluación de Modelos")
    st.markdown("---")
    
    if 'historial_ml' not in st.session_state:
        st.session_state.historial_ml = []
        
    func_sel = st.selectbox("Función:", ["Calcular Métricas de Clasificación"])
    modelo = st.text_input("Nombre del Modelo (Ej. Random Forest):")
    
    st.write("Matriz de Confusión:")
    c1, c2, c3 = st.columns(3)
    with c1: tp = st.number_input("TP", min_value=0, step=1)
    with c2: fp = st.number_input("FP", min_value=0, step=1)
    with c3: fn = st.number_input("FN", min_value=0, step=1)
        
    if st.button("Evaluar"):
        if not modelo.strip():
            st.warning("Ingresa el nombre del modelo.")
        else:
            try:
                res = calcular_metricas_clasificacion(tp, fp, fn)
                
                st.write(f"**Resultados: {modelo}**")
                m1, m2, m3 = st.columns(3)
                m1.metric("Precisión", f"{res['precision']:.4f}")
                m2.metric("Recall", f"{res['recall']:.4f}")
                m3.metric("F1-Score", f"{res['f1_score']:.4f}")
                
                st.session_state.historial_ml.append({
                    "Modelo": modelo,
                    "TP": tp, "FP": fp, "FN": fn,
                    "Precisión": res['precision'],
                    "Recall": res['recall'],
                    "F1-Score": res['f1_score']
                })
                
            except Exception as e:
                st.error(f"Error en cálculo: {e}")
                
    st.markdown("---")
    
    if st.session_state.historial_ml:
        st.subheader("Historial de Evaluaciones")
        st.dataframe(pd.DataFrame(st.session_state.historial_ml), use_container_width=True)

# ==========================================
# EJERCICIO 4: CRUD POO
# ==========================================
elif opcion == "Ejercicio 4":
    st.header("Gestión de Inventario (CRUD)")
    st.markdown("---")
    
    if 'db_inventario' not in st.session_state:
        st.session_state.db_inventario = {}
        
    t_crear, t_leer, t_act, t_elim = st.tabs(["Crear", "Leer", "Actualizar", "Eliminar"])
    
    # --- CREATE ---
    with t_crear:
        c1, c2 = st.columns(2)
        with c1:
            n_prod = st.text_input("Producto:")
            c_unit = st.number_input("Costo Unitario:", min_value=0.0, step=1.0)
        with c2:
            p_unit = st.number_input("Precio Unitario:", min_value=0.0, step=1.0)
            s_act = st.number_input("Stock Actual:", min_value=0, step=1)
            s_min = st.number_input("Stock Min:", min_value=0, step=1)
            
        if st.button("Guardar Producto"):
            if not n_prod.strip():
                st.warning("Falta nombre.")
            elif n_prod in st.session_state.db_inventario:
                st.warning("El producto ya existe.")
            else:
                try:
                    obj_prod = InventarioProducto(n_prod, c_unit, p_unit, s_act, s_min)
                    st.session_state.db_inventario[n_prod] = obj_prod
                    st.success("Guardado.")
                except ValueError as e:
                    st.error(f"Error: {e}")

    # --- READ ---
    with t_leer:
        if st.session_state.db_inventario:
            data = [p.resumen() for p in st.session_state.db_inventario.values()]
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.info("Sin registros.")

    # --- UPDATE ---
    with t_act:
        if st.session_state.db_inventario:
            target = st.selectbox("Seleccionar producto:", list(st.session_state.db_inventario.keys()))
            item = st.session_state.db_inventario[target]
            
            c1, c2 = st.columns(2)
            with c1:
                new_cost = st.number_input("Costo:", min_value=0.0, value=float(item.costo_unitario))
                new_price = st.number_input("Precio:", min_value=0.0, value=float(item.precio_unitario))
            with c2:
                new_stock = st.number_input("Stock:", min_value=0, value=int(item.stock_actual))
                new_min = st.number_input("Stock Min:", min_value=0, value=int(item.stock_minimo))
                
            if st.button("Actualizar"):
                try:
                    item_updated = InventarioProducto(target, new_cost, new_price, new_stock, new_min)
                    st.session_state.db_inventario[target] = item_updated
                    st.success("Actualizado.")
                except ValueError as e:
                    st.error(f"Error: {e}")

    # --- DELETE ---
    with t_elim:
        if st.session_state.db_inventario:
            target_del = st.selectbox("Eliminar producto:", list(st.session_state.db_inventario.keys()), key="del")
            if st.button("Eliminar"):
                del st.session_state.db_inventario[target_del]
                st.success("Eliminado.")