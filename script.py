import requests
import json
from typing import Optional, Dict, Any

# URL base del servicio FastAPI
BASE_URL = "http://localhost:8000"


# Colores para la terminal (opcional, para mejor visualización)
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def print_response(title: str, response: requests.Response, color: str = Colors.BLUE):
    """Imprime la respuesta de manera formateada"""
    print(f"\n{color}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{Colors.RESET}")
    print(f"Status Code: {response.status_code}")

    try:
        data = response.json()
        print(f"Response:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


# ----------------------------------------------------
# 0. HEALTH CHECK
# ----------------------------------------------------
def health_check():
    """Verificar el estado del servicio"""
    print(f"\n{Colors.YELLOW}>>> Verificando estado del servicio...{Colors.RESET}")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response("HEALTH CHECK", response, Colors.GREEN)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(
            f"{Colors.RED}Error de conexión. Asegúrate de que el servicio esté corriendo en {BASE_URL}{Colors.RESET}"
        )
        return False
    except Exception as e:
        print(f"{Colors.RED}Ocurrió un error inesperado: {e}{Colors.RESET}")
        return False


# ----------------------------------------------------
# 1. CREATE - Crear usuario (POST)
# ----------------------------------------------------
def create_user(email: str, password: str) -> Optional[Dict[Any, Any]]:
    """Crear un nuevo usuario"""
    print(f"\n{Colors.YELLOW}>>> Creando usuario con email: {email}{Colors.RESET}")

    url = f"{BASE_URL}/users/"
    payload = {"email": email, "password": password}

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 201:
            print_response(
                "✓ USUARIO CREADO EXITOSAMENTE (POST)", response, Colors.GREEN
            )
            return response.json()
        elif response.status_code == 400:
            print_response("✗ ERROR: Email ya registrado (POST)", response, Colors.RED)
            return None
        else:
            print_response(f"✗ ERROR AL CREAR USUARIO (POST)", response, Colors.RED)
            return None

    except requests.exceptions.ConnectionError:
        print(
            f"{Colors.RED}Error de conexión. Asegúrate de que el servicio esté corriendo{Colors.RESET}"
        )
        return None
    except Exception as e:
        print(f"{Colors.RED}Ocurrió un error inesperado: {e}{Colors.RESET}")
        return None


# ----------------------------------------------------
# 2. READ ALL - Obtener todos los usuarios (GET)
# ----------------------------------------------------
def get_all_users(skip: int = 0, limit: int = 100):
    """Obtener lista de todos los usuarios con paginación"""
    print(
        f"\n{Colors.YELLOW}>>> Obteniendo todos los usuarios (skip={skip}, limit={limit})...{Colors.RESET}"
    )

    url = f"{BASE_URL}/users/"
    params = {"skip": skip, "limit": limit}

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            print_response("✓ LISTA DE USUARIOS OBTENIDA (GET)", response, Colors.GREEN)
            return response.json()
        else:
            print_response("✗ ERROR AL OBTENER USUARIOS (GET)", response, Colors.RED)
            return None

    except requests.exceptions.ConnectionError:
        print(
            f"{Colors.RED}Error de conexión. Asegúrate de que el servicio esté corriendo{Colors.RESET}"
        )
        return None
    except Exception as e:
        print(f"{Colors.RED}Ocurrió un error inesperado: {e}{Colors.RESET}")
        return None


# ----------------------------------------------------
# 3. READ ONE - Obtener un usuario por ID (GET)
# ----------------------------------------------------
def get_user_by_id(user_id: int):
    """Obtener un usuario específico por su ID"""
    print(f"\n{Colors.YELLOW}>>> Obteniendo usuario con ID: {user_id}...{Colors.RESET}")

    url = f"{BASE_URL}/users/{user_id}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            print_response(
                f"✓ USUARIO (ID: {user_id}) ENCONTRADO (GET)", response, Colors.GREEN
            )
            return response.json()
        elif response.status_code == 404:
            print_response(
                f"✗ USUARIO (ID: {user_id}) NO ENCONTRADO (GET)", response, Colors.RED
            )
            return None
        else:
            print_response(f"✗ ERROR AL OBTENER USUARIO (GET)", response, Colors.RED)
            return None

    except requests.exceptions.ConnectionError:
        print(
            f"{Colors.RED}Error de conexión. Asegúrate de que el servicio esté corriendo{Colors.RESET}"
        )
        return None
    except Exception as e:
        print(f"{Colors.RED}Ocurrió un error inesperado: {e}{Colors.RESET}")
        return None


# ----------------------------------------------------
# 4. UPDATE - Actualizar usuario (PATCH)
# ----------------------------------------------------
def update_user(user_id: int, **kwargs):
    """
    Actualizar información de un usuario

    Parámetros opcionales:
    - email: str
    - password: str
    - is_active: bool
    - is_verified: bool
    """
    print(
        f"\n{Colors.YELLOW}>>> Actualizando usuario con ID: {user_id}...{Colors.RESET}"
    )

    url = f"{BASE_URL}/users/{user_id}"
    payload = {k: v for k, v in kwargs.items() if v is not None}

    if not payload:
        print(
            f"{Colors.RED}Error: No se proporcionaron campos para actualizar{Colors.RESET}"
        )
        return None

    try:
        response = requests.patch(url, json=payload)

        if response.status_code == 200:
            print_response(
                f"✓ USUARIO (ID: {user_id}) ACTUALIZADO (PATCH)", response, Colors.GREEN
            )
            return response.json()
        elif response.status_code == 404:
            print_response(
                f"✗ USUARIO (ID: {user_id}) NO ENCONTRADO (PATCH)", response, Colors.RED
            )
            return None
        else:
            print_response(
                f"✗ ERROR AL ACTUALIZAR USUARIO (PATCH)", response, Colors.RED
            )
            return None

    except requests.exceptions.ConnectionError:
        print(
            f"{Colors.RED}Error de conexión. Asegúrate de que el servicio esté corriendo{Colors.RESET}"
        )
        return None
    except Exception as e:
        print(f"{Colors.RED}Ocurrió un error inesperado: {e}{Colors.RESET}")
        return None


# ----------------------------------------------------
# 5. DELETE - Eliminar usuario / Soft Delete (DELETE)
# ----------------------------------------------------
def delete_user(user_id: int):
    """Desactivar un usuario (soft delete)"""
    print(
        f"\n{Colors.YELLOW}>>> Eliminando (desactivando) usuario con ID: {user_id}...{Colors.RESET}"
    )

    url = f"{BASE_URL}/users/{user_id}"

    try:
        response = requests.delete(url)

        if response.status_code == 200:
            print_response(
                f"✓ USUARIO (ID: {user_id}) DESACTIVADO (DELETE)",
                response,
                Colors.GREEN,
            )
            return response.json()
        elif response.status_code == 404:
            print_response(
                f"✗ USUARIO (ID: {user_id}) NO ENCONTRADO (DELETE)",
                response,
                Colors.RED,
            )
            return None
        else:
            print_response(
                f"✗ ERROR AL ELIMINAR USUARIO (DELETE)", response, Colors.RED
            )
            return None

    except requests.exceptions.ConnectionError:
        print(
            f"{Colors.RED}Error de conexión. Asegúrate de que el servicio esté corriendo{Colors.RESET}"
        )
        return None
    except Exception as e:
        print(f"{Colors.RED}Ocurrió un error inesperado: {e}{Colors.RESET}")
        return None


# ----------------------------------------------------
# FUNCIÓN PRINCIPAL - DEMO COMPLETA
# ----------------------------------------------------
def run_demo():
    """Ejecutar demostración completa de todos los endpoints CRUD"""

    print(f"\n{Colors.BLUE}{'='*60}")
    print("DEMOSTRACIÓN COMPLETA DE CRUD - CatalogIA Users API")
    print(f"{'='*60}{Colors.RESET}")

    # 0. Health Check
    if not health_check():
        print(
            f"\n{Colors.RED}No se pudo conectar al servicio. Abortando demo.{Colors.RESET}"
        )
        return

    # 1. CREATE - Crear varios usuarios
    print(f"\n{Colors.BLUE}--- PASO 1: CREAR USUARIOS (POST) ---{Colors.RESET}")
    user1 = create_user("alice@example.com", "password123")
    user2 = create_user("bob@example.com", "securepass456")
    user3 = create_user("charlie@example.com", "mypassword789")

    # Intentar crear usuario duplicado
    print(f"\n{Colors.BLUE}--- Intentando crear usuario duplicado ---{Colors.RESET}")
    duplicate = create_user("alice@example.com", "password123")

    # 2. READ ALL - Obtener todos los usuarios
    print(
        f"\n{Colors.BLUE}--- PASO 2: OBTENER TODOS LOS USUARIOS (GET) ---{Colors.RESET}"
    )
    all_users = get_all_users()

    # 3. READ ONE - Obtener usuario específico
    if user1:
        print(
            f"\n{Colors.BLUE}--- PASO 3: OBTENER USUARIO POR ID (GET) ---{Colors.RESET}"
        )
        get_user_by_id(user1["user_id"])

    # Intentar obtener usuario que no existe
    print(
        f"\n{Colors.BLUE}--- Intentando obtener usuario inexistente ---{Colors.RESET}"
    )
    get_user_by_id(9999)

    # 4. UPDATE - Actualizar usuario
    if user2:
        print(
            f"\n{Colors.BLUE}--- PASO 4: ACTUALIZAR USUARIO (PATCH) ---{Colors.RESET}"
        )

        # Actualizar solo verificación
        update_user(user2["user_id"], is_verified=True)

        # Actualizar múltiples campos
        if user3:
            update_user(
                user3["user_id"],
                email="charlie.updated@example.com",
                is_verified=True,
                is_active=True,
            )

    # 5. DELETE - Soft delete de usuario
    if user1:
        print(
            f"\n{Colors.BLUE}--- PASO 5: ELIMINAR USUARIO (DELETE - Soft Delete) ---{Colors.RESET}"
        )
        delete_user(user1["user_id"])

        # Verificar que el usuario sigue existiendo pero está inactivo
        print(
            f"\n{Colors.BLUE}--- Verificando que el usuario eliminado existe pero está inactivo ---{Colors.RESET}"
        )
        get_user_by_id(user1["user_id"])

    # 6. Mostrar estado final
    print(f"\n{Colors.BLUE}--- ESTADO FINAL: TODOS LOS USUARIOS ---{Colors.RESET}")
    get_all_users()

    print(f"\n{Colors.GREEN}{'='*60}")
    print("DEMOSTRACIÓN COMPLETADA")
    print(f"{'='*60}{Colors.RESET}\n")


# ----------------------------------------------------
# PUNTO DE ENTRADA
# ----------------------------------------------------
if __name__ == "__main__":
    run_demo()
