
# Custom Authentication & RBAC System

## Стек
- Django 4.2
- Django REST Framework
- SQLite
- JWT (ручная реализация, без встроенного auth фреймворка)
- Собственная RBAC система

## Запуск
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py init_demo_data  # Загрузка тестовых данных
python3 manage.py runserver
```

Админ: `login: admin@test.com` / `password: admin123`

---

## Схема разграничения прав доступа (RBAC)

Система построена по модели **Role-Based Access Control**: доступ к ресурсам определяется не напрямую пользователем, а через роли. Правило доступа задаётся парой **ресурс + действие** (permission).

### Составляющие схемы

| Сущность | Описание |
|----------|----------|
| **User** | Пользователь (email, имя, фамилия, отчество, is_active). Не хранит права напрямую. |
| **Role** | Роль (например: `admin`, `user`). Группирует набор разрешений. |
| **Permission** | Разрешение: пара `(resource, action)`. Определяет, *к какому ресурсу* и *какое действие* разрешено (например: `articles:read`, `rbac:manage`). |
| **UserRole** | Связь «пользователь — роль». У пользователя может быть несколько ролей. |
| **RolePermission** | Связь «роль — разрешение». Правило: «роль R даёт разрешение P». |

### Правило доступа

Пользователю разрешено действие над ресурсом тогда и только тогда, когда у него есть хотя бы одна роль, у которой есть разрешение.

- **Ресурс** — имя объекта (например: `articles`, `reports`, `rbac`).
- **Действие** — тип операции (например: `read`, `write`, `manage`).

### Ошибки HTTP

- **401 Unauthorized** — по запросу не удалось определить залогиненного пользователя (нет/неверный токен, пользователь не найден или `is_active=False`).
- **403 Forbidden** — пользователь определён, но у него нет нужного разрешения (resource, action) по правилам RBAC.

---

## API

### Пользователь (без токена для register/login)
- `POST /api/users/register/` — регистрация (email, password, password_confirm, first_name, last_name, patronymic).
- `POST /api/users/login/` — вход (email, password), в ответе JWT-токен.

### Пользователь (с заголовком `Authorization: Bearer <token>`)
- `POST /api/users/logout/` — выход (клиент отбрасывает токен).
- `GET /api/users/profile/` — текущий профиль.
- `PATCH /api/users/profile/` — обновление профиля.
- `POST /api/users/delete-account/` — мягкое удаление (is_active=False), после этого вход невозможен.

### Мок-ресурсы (проверка прав)
- `GET /api/articles/` — список статей (требуется разрешение `articles:read`).
- `GET /api/reports/` — список отчётов (требуется разрешение `reports:read`; в демо только у admin).

### Админ RBAC (требуется разрешение `rbac:manage`)
- `GET/POST /api/admin/roles/` — список ролей, создание роли.
- `GET/PATCH/DELETE /api/admin/roles/<id>/` — просмотр/изменение/удаление роли.
- `GET/POST /api/admin/permissions/` — список разрешений, создание разрешения.
- `GET /api/admin/roles/<id>/permissions/` — список разрешений роли (правила доступа роли).
- `POST /api/admin/roles/<id>/permissions/add/` — добавить разрешение роли (body: `permission_id`).
- `DELETE /api/admin/roles/<id>/permissions/<permission_id>/` — удалить разрешение у роли.
- `POST /api/admin/users/<user_id>/roles/` — назначить роль пользователю (body: `role_id`).
