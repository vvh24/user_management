## User Search and Filtering API Documentation

### Endpoint
**`GET /users`**

### Description
This endpoint allows administrators to search for and filter users based on various attributes such as nickname, email, role, and more. It also supports advanced full-text search, pagination, and sorting to manage large datasets efficiently.

---

### Parameters

| Parameter           | Type    | Required | Description                                                 |
|---------------------|---------|----------|-------------------------------------------------------------|
| `nickname`          | string  | No       | Partial match on the user's nickname.                      |
| `email`             | string  | No       | Partial match on the user's email address.                 |
| `role`              | string  | No       | Filter by user role (`ADMIN`, `MANAGER`, etc.).            |
| `is_locked`         | boolean | No       | Filter by account lock status.                             |
| `created_at_start`  | string  | No       | Start of the registration date range (ISO 8601 format).    |
| `created_at_end`    | string  | No       | End of the registration date range (ISO 8601 format).      |
| `search_term`       | string  | No       | Full-text search term.                                      |
| `skip`              | integer | No       | Number of records to skip for pagination.                  |
| `limit`             | integer | No       | Number of records to return for pagination.                |
| `sort_field`        | string  | No       | Field to sort by (e.g., `nickname`, `created_at`).          |
| `sort_direction`    | string  | No       | Sort direction (`asc` or `desc`).                          |

---

### Example Request

```http
GET /users?search_term=programming&role=ADMIN&sort_field=created_at&sort_direction=asc&skip=0&limit=10
```

---

### Example Response

```json
[
  {
    "id": "1b3e7bcd-7843-42f8-905b-b9de3f8e34b5",
    "nickname": "valeria",
    "email": "valeria@example.com",
    "role": "ADMIN",
    "is_locked": false,
    "created_at": "2024-12-10T12:00:00Z",
    "updated_at": "2024-12-16T12:00:00Z"
  }
]
```

---

## Reflection Document

### New Feature: User Search and Filtering

#### Purpose
The User Search and Filtering feature is designed to empower administrators to efficiently locate and manage users in the system. By providing flexible filtering options and a robust full-text search mechanism, this feature enhances the administrator's ability to maintain order and ensure optimal user management.

#### Usage
Administrators can utilize the API to search for users by nickname, email, or role. They can filter results by account status, date ranges, and more. Pagination and sorting options allow for refined control when working with extensive user lists.

#### Configuration
This feature uses PostgreSQL's full-text search capabilities. The `search_vector` column in the `users` table enables efficient full-text indexing and searching. Developers can configure the feature by:
1. Setting up the database migrations to include the `search_vector` column.
2. Adding the `search_users` method to the `UserService` class.
3. Using filters and query parameters in the API request for tailored results.

---

### Reflection on Implementation

#### Learnings
Implementing the User Search and Filtering feature provided valuable insights into database optimization and the practical application of full-text search using PostgreSQL. It also highlighted the importance of maintaining clean and reusable code in service methods, as well as the significance of API documentation for usability. For this project, the helped of ChatGPT was a plus since it helped me going through every error, I encountered during the way and helped me not only solved it, but understand why I was doing what I did, the importance behind it, and also being more aware of the changes I was making in order for the feature implemented (user search and filtering) to work. 

#### Challenges and Solutions
1. **Database Migration Errors**: The `users` table was initially missing, causing test failures. This was resolved by verifying migrations and re-applying them correctly.
2. **Full-Text Search Syntax**: Understanding PostgreSQL's full-text search syntax took time. Using the `plainto_tsquery` function resolved issues with query formulation.
3. **Testing Failures**: Tests failed due to duplicate data and improper cleanup. Fixtures were adjusted to ensure a clean state for each test.

---

### DockerHub Deployment

#### Deployment Link
[DockerHub Deployment Link](https://hub.docker.com/r/your_dockerhub_username/your_repository_name)

#### Evidence of Successful Deployment
![Successful Deployment Screenshot](path/to/screenshot.png)

#### Steps to Deploy
1. Build the Docker image using `docker build -t your_dockerhub_username/your_repository_name .`.
2. Push the image to DockerHub using `docker push your_dockerhub_username/your_repository_name`.
3. Ensure the deployment is running and accessible via the provided API endpoint.

---
