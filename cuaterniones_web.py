# cuaterniones_web.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ===== Clase Quaternion =====
class Quaternion:
    def __init__(self, a, b, c, d):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)

    def __str__(self):
        return f"{self.a} + {self.b}i + {self.c}j + {self.d}k"

    def __add__(self, other):
        return Quaternion(self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d)

    def __sub__(self, other):
        return Quaternion(self.a - other.a, self.b - other.b, self.c - other.c, self.d - other.d)

    def __mul__(self, other):
        a1, b1, c1, d1 = self.a, self.b, self.c, self.d
        a2, b2, c2, d2 = other.a, other.b, other.c, other.d
        return Quaternion(
            a1*a2 - b1*b2 - c1*c2 - d1*d2,
            a1*b2 + b1*a2 + c1*d2 - d1*c2,
            a1*c2 - b1*d2 + c1*a2 + d1*b2,
            a1*d2 + b1*c2 - c1*b2 + d1*a2
        )

    def conjugate(self):
        return Quaternion(self.a, -self.b, -self.c, -self.d)

    def norm(self):
        return np.sqrt(self.a**2 + self.b**2 + self.c**2 + self.d**2)

    def inverse(self):
        n2 = self.norm() ** 2
        if n2 == 0:
            raise ZeroDivisionError("No se puede invertir un cuaternión de norma 0.")
        conj = self.conjugate()
        return Quaternion(conj.a / n2, conj.b / n2, conj.c / n2, conj.d / n2)

    def normalize(self):
        n = self.norm()
        if n == 0:
            raise ZeroDivisionError("No se puede normalizar un cuaternión de norma 0.")
        return Quaternion(self.a / n, self.b / n, self.c / n, self.d / n)

    def to_vector(self):
        return np.array([self.b, self.c, self.d])

# ===== Funciones =====
def rotate_vector(v, q: Quaternion):
    qn = q.normalize()
    q_vec = Quaternion(0, *v)
    q_rotated = qn * q_vec * qn.inverse()
    return q_rotated.to_vector()

def plot_vectors(original, rotated):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.quiver(0, 0, 0, original[0], original[1], original[2], color='r', label='Original')
    ax.quiver(0, 0, 0, rotated[0], rotated[1], rotated[2], color='b', label='Rotado')

    max_range = max(np.abs(original).max(), np.abs(rotated).max(), 1)
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    st.pyplot(fig)

# ===== Interfaz Web =====
st.set_page_config(page_title="Calculadora de Cuaterniones", layout="centered")

st.title("⚙️ Calculadora de Cuaterniones")
st.markdown("Operaciones básicas y rotación de vectores usando cuaterniones.")

st.subheader("Ingresar Cuaternión A")
a_a = st.number_input("a (A)", value=1.0)
b_a = st.number_input("b (A)", value=0.0)
c_a = st.number_input("c (A)", value=0.0)
d_a = st.number_input("d (A)", value=0.0)

st.subheader("Ingresar Cuaternión B")
a_b = st.number_input("a (B)", value=0.0)
b_b = st.number_input("b (B)", value=0.0)
c_b = st.number_input("c (B)", value=0.0)
d_b = st.number_input("d (B)", value=0.0)

A = Quaternion(a_a, b_a, c_a, d_a)
B = Quaternion(a_b, b_b, c_b, d_b)

st.markdown("### Operaciones")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Sumar (A + B)"):
        st.success(f"Suma: {A + B}")

with col2:
    if st.button("➖ Restar (A - B)"):
        st.success(f"Resta: {A - B}")

with col3:
    if st.button("✖️ Multiplicar (A * B)"):
        st.success(f"Multiplicación: {A * B}")

st.markdown("---")
st.subheader("Rotar un vector con Cuaternión A")
x = st.number_input("x", value=1.0)
y = st.number_input("y", value=0.0)
z = st.number_input("z", value=0.0)

if st.button("🔄 Rotar Vector"):
    try:
        v = np.array([x, y, z])
        v_rot = rotate_vector(v, A)
        st.success(f"Vector Rotado: {v_rot}")
        plot_vectors(v, v_rot)
    except Exception as e:
        st.error(str(e))
