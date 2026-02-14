# BÁO CÁO MIGRATION: FASTAPI TO SPRING BOOT

## Thông Tin Đồ Án

**Tên đồ án:** Migration ứng dụng API từ FastAPI sang Spring Boot  
**Sinh viên thực hiện:** [Tên sinh viên]  
**Lớp:** [Tên lớp]  
**Môn học:** Seminar Chuyên Đề  
**Ngày hoàn thành:** 12/02/2026

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1. Mục tiêu
Dự án thực hiện migration (di chuyển) một ứng dụng Social Media API từ nền tảng Python FastAPI sang Java Spring Boot, đảm bảo tính tương thích hoàn toàn về chức năng, API endpoints, và OpenAPI specification.

### 1.2. Yêu cầu chính
- ✅ Migration toàn bộ endpoints từ FastAPI sang Spring Boot
- ✅ Đảm bảo API endpoints giữ nguyên cấu trúc và chức năng
- ✅ Sử dụng SQLite database với tên file `sns_api.db`
- ✅ Database được khởi tạo lại mỗi khi start application
- ✅ Render Swagger UI tại default endpoint
- ✅ Render OpenAPI document đúng theo file `openapi.yaml`
- ✅ Không thêm/xóa/sửa bất kỳ định nghĩa nào trong `openapi.yaml`

---

## 2. PHÂN TÍCH ỨNG DỤNG NGUỒN (FastAPI)

### 2.1. Cấu trúc ứng dụng Python
```
python/
├── main.py           # API endpoints và FastAPI configuration
├── models.py         # Pydantic models cho request/response
├── database.py       # Database operations với SQLite
└── openapi.yaml      # OpenAPI specification
```

### 2.2. Công nghệ sử dụng (Source)
- **Framework:** FastAPI
- **Language:** Python 3.x
- **Database:** SQLite
- **ORM/Database Access:** Raw SQL với sqlite3
- **Validation:** Pydantic models
- **API Documentation:** FastAPI built-in Swagger UI

### 2.3. Các chức năng chính
1. **Post Management:**
   - GET `/api/posts` - Liệt kê tất cả posts
   - POST `/api/posts` - Tạo post mới
   - GET `/api/posts/{postId}` - Lấy chi tiết post
   - PATCH `/api/posts/{postId}` - Cập nhật post
   - DELETE `/api/posts/{postId}` - Xóa post

2. **Comment Management:**
   - GET `/api/posts/{postId}/comments` - Liệt kê comments của post
   - POST `/api/posts/{postId}/comments` - Tạo comment mới
   - GET `/api/posts/{postId}/comments/{commentId}` - Lấy chi tiết comment
   - PATCH `/api/posts/{postId}/comments/{commentId}` - Cập nhật comment
   - DELETE `/api/posts/{postId}/comments/{commentId}` - Xóa comment

3. **Like System:**
   - POST `/api/posts/{postId}/likes` - Like một post
   - DELETE `/api/posts/{postId}/likes` - Unlike một post

---

## 3. THIẾT KẾ ỨNG DỤNG MỚI (Spring Boot)

### 3.1. Cấu trúc ứng dụng Java
```
java/socialapp/src/main/java/com/contoso/socialapp/
├── config/
│   ├── CorsConfig.java           # CORS configuration
│   ├── DatabaseConfig.java       # Database initialization
│   └── OpenApiConfig.java        # OpenAPI/Swagger configuration
├── controller/
│   ├── PostController.java       # Post endpoints
│   ├── CommentController.java    # Comment endpoints
│   └── LikeController.java       # Like endpoints
├── dto/
│   ├── CreatePostRequest.java    # Request DTOs
│   ├── UpdatePostRequest.java
│   ├── CreateCommentRequest.java
│   ├── UpdateCommentRequest.java
│   ├── PostResponse.java         # Response DTOs
│   ├── CommentResponse.java
│   └── LikeResponse.java
├── entity/
│   ├── Post.java                 # JPA entities
│   ├── Comment.java
│   └── Like.java
├── repository/
│   ├── PostRepository.java       # JPA repositories
│   ├── CommentRepository.java
│   └── LikeRepository.java
├── service/
│   ├── PostService.java          # Business logic
│   ├── CommentService.java
│   └── LikeService.java
├── exception/
│   ├── ResourceNotFoundException.java
│   └── ValidationException.java
└── SocialappApplication.java     # Main application class
```

### 3.2. Công nghệ sử dụng (Target)
- **Framework:** Spring Boot 3.5.0
- **Language:** Java 25
- **Build Tool:** Gradle
- **Database:** SQLite
- **ORM:** Spring Data JPA + Hibernate
- **Database Dialect:** Hibernate Community SQLite Dialect
- **API Documentation:** SpringDoc OpenAPI 2.7.0
- **Validation:** Jakarta Bean Validation
- **Utilities:** Lombok

### 3.3. Dependencies chính (build.gradle)
```gradle
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.xerial:sqlite-jdbc:3.47.1.0'
    implementation 'org.hibernate.orm:hibernate-community-dialects:6.6.4.Final'
    implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.7.0'
    compileOnly 'org.projectlombok:lombok'
    annotationProcessor 'org.projectlombok:lombok'
}
```

---

## 4. QUÁ TRÌNH MIGRATION

### 4.1. Các bước thực hiện

#### Bước 1: Phân tích cấu trúc ứng dụng FastAPI
- Xem xét file `product-requirements.md` để hiểu business requirements
- Phân tích `openapi.yaml` để nắm rõ API specification
- Đọc source code Python để hiểu logic nghiệp vụ
- Xác định database schema và relationships

#### Bước 2: Setup Spring Boot project
- Khởi tạo Spring Boot project với Gradle
- Cấu hình Java 25 và Spring Boot 3.5.0
- Thêm dependencies cần thiết cho JPA, SQLite, OpenAPI

#### Bước 3: Thiết kế kiến trúc Spring Boot
- Áp dụng kiến trúc layered: Controller → Service → Repository
- Tạo package structure theo best practices
- Định nghĩa DTOs cho request/response
- Tạo JPA entities và repositories

#### Bước 4: Migration Database Layer
- Chuyển đổi raw SQL sang JPA entities
- Implement DatabaseConfig với @PostConstruct để khởi tạo database
- Tạo 3 tables: `posts`, `comments`, `likes` với đúng schema
- Cấu hình foreign keys và cascading

#### Bước 5: Migration Business Logic
- Chuyển đổi các hàm trong database.py sang Service classes
- Implement PostService, CommentService, LikeService
- Xử lý validation và error handling
- Đảm bảo logic nghiệp vụ giống hệt FastAPI

#### Bước 6: Migration API Endpoints
- Tạo Controllers cho Posts, Comments, Likes
- Map từng endpoint FastAPI sang Spring Boot controllers
- Sử dụng annotations: @RestController, @RequestMapping, @GetMapping, etc.
- Thêm OpenAPI annotations từ SpringDoc

#### Bước 7: Cấu hình OpenAPI và Swagger UI
- Cấu hình OpenApiConfig để match với openapi.yaml
- Setup Swagger UI tại `/swagger-ui.html`
- Cấu hình OpenAPI JSON tại `/openapi.json`
- Đảm bảo metadata (title, description, contact) giống hệt

#### Bước 8: Testing và Validation
- Test từng endpoint với Postman/curl
- Verify response structure matches OpenAPI spec
- Kiểm tra database initialization
- Test error handling và validation

### 4.2. Sử dụng GitHub Copilot và Context7

Trong quá trình migration, đã sử dụng:
- **GitHub Copilot Agent Mode** với Claude Sonnet 4 để:
  - Phân tích code structure
  - Generate boilerplate code
  - Suggest best practices cho Spring Boot
  
- **Context7 MCP Server** để:
  - Tra cứu documentation của Spring Boot
  - Tìm hiểu về Spring Data JPA patterns
  - Reference SpringDoc OpenAPI configuration

---

## 5. CHI TIẾT TECHNICAL IMPLEMENTATION

### 5.1. Database Configuration

**File:** `DatabaseConfig.java`
```java
@PostConstruct
public void initializeDatabase() {
    // Drop existing tables để đảm bảo fresh start
    jdbcTemplate.execute("DROP TABLE IF EXISTS likes");
    jdbcTemplate.execute("DROP TABLE IF EXISTS comments");
    jdbcTemplate.execute("DROP TABLE IF EXISTS posts");
    
    // Create tables với đúng schema
    // Áp dụng foreign keys và ON DELETE CASCADE
}
```

**Điểm đặc biệt:**
- Database được khởi tạo lại mỗi lần start app (yêu cầu của đề bài)
- Sử dụng JdbcTemplate để execute raw SQL
- Drop tables theo thứ tự đúng (tránh foreign key constraint errors)

### 5.2. JPA Entities

**Example:** `Post.java`
```java
@Entity
@Table(name = "posts")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Post {
    @Id
    private String id;
    
    @Column(nullable = false, length = 50)
    private String username;
    
    @Column(nullable = false, length = 1000)
    private String content;
    
    @Column(name = "created_at", nullable = false)
    private String createdAt;
    
    @Column(name = "updated_at", nullable = false)
    private String updatedAt;
    
    @PrePersist
    public void prePersist() {
        if (id == null) {
            id = UUID.randomUUID().toString();
        }
        String now = Instant.now().toString();
        if (createdAt == null) {
            createdAt = now;
        }
        updatedAt = now;
    }
}
```

**Highlights:**
- Sử dụng Lombok để reduce boilerplate code
- UUID auto-generation trong @PrePersist
- Timestamps tự động với ISO-8601 format

### 5.3. Service Layer Pattern

Áp dụng separation of concerns:
- **Controllers:** Chỉ xử lý HTTP requests/responses
- **Services:** Chứa business logic
- **Repositories:** Data access layer

Example service method:
```java
public PostResponse createPost(CreatePostRequest request) {
    Post post = new Post();
    post.setUsername(request.getUsername());
    post.setContent(request.getContent());
    post.prePersist();
    
    Post savedPost = postRepository.save(post);
    return mapToResponse(savedPost);
}
```

### 5.4. Exception Handling

Tạo custom exceptions:
- `ResourceNotFoundException` - cho 404 errors
- `ValidationException` - cho 400 errors

Sử dụng @ControllerAdvice để global exception handling.

### 5.5. OpenAPI Configuration

**File:** `OpenApiConfig.java`
```java
@Bean
public OpenAPI customOpenAPI() {
    return new OpenAPI()
        .info(new Info()
            .title("Simple Social Media Application API")
            .description("A basic SNS API...")
            .version("1.0.0")
            .contact(new Contact()
                .name("Contoso Product Team")
                .email("tech-lead@contoso.com")))
        .servers(List.of(
            new Server()
                .url("http://localhost:8080/api")
                .description("Local development server")));
}
```

**application.properties:**
```properties
springdoc.api-docs.path=/openapi.json
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.swagger-ui.operationsSorter=alpha
springdoc.swagger-ui.tagsSorter=alpha
```

---

## 6. SO SÁNH FASTAPI VS SPRING BOOT

| Aspect | FastAPI (Python) | Spring Boot (Java) |
|--------|------------------|-------------------|
| **Framework Type** | Async, modern Python web framework | Enterprise-grade Java framework |
| **Routing** | Function decorators (@app.get) | Annotations (@GetMapping) |
| **Validation** | Pydantic models | Jakarta Bean Validation + DTOs |
| **ORM/Database** | Raw SQL với sqlite3 | Spring Data JPA + Hibernate |
| **Dependency Injection** | Manual/FastAPI depends | Spring IoC Container |
| **API Documentation** | Built-in với Pydantic | SpringDoc OpenAPI |
| **Error Handling** | HTTPException | @ControllerAdvice + Custom Exceptions |
| **Type Safety** | Runtime (Python duck typing) | Compile-time (Java static typing) |
| **Performance** | Fast startup, async | Slower startup, thread-based |
| **Code Volume** | Ít code hơn, concise | Nhiều boilerplate, verbose |
| **Enterprise Features** | Limited | Extensive (Security, Actuator, etc.) |

---

## 7. MAPPING ENDPOINTS

### 7.1. Posts Endpoints

| HTTP Method | Endpoint | FastAPI Handler | Spring Boot Controller |
|-------------|----------|----------------|----------------------|
| GET | `/api/posts` | `get_posts()` | `PostController.getAllPosts()` |
| POST | `/api/posts` | `create_new_post()` | `PostController.createPost()` |
| GET | `/api/posts/{postId}` | `get_post_by_id_endpoint()` | `PostController.getPostById()` |
| PATCH | `/api/posts/{postId}` | `update_post_endpoint()` | `PostController.updatePost()` |
| DELETE | `/api/posts/{postId}` | `delete_post_endpoint()` | `PostController.deletePost()` |

### 7.2. Comments Endpoints

| HTTP Method | Endpoint | FastAPI Handler | Spring Boot Controller |
|-------------|----------|----------------|----------------------|
| GET | `/api/posts/{postId}/comments` | `get_comments_by_post_id_endpoint()` | `CommentController.getCommentsByPostId()` |
| POST | `/api/posts/{postId}/comments` | `create_comment_endpoint()` | `CommentController.createComment()` |
| GET | `/api/posts/{postId}/comments/{commentId}` | `get_comment_by_id_endpoint()` | `CommentController.getCommentById()` |
| PATCH | `/api/posts/{postId}/comments/{commentId}` | `update_comment_endpoint()` | `CommentController.updateComment()` |
| DELETE | `/api/posts/{postId}/comments/{commentId}` | `delete_comment_endpoint()` | `CommentController.deleteComment()` |

### 7.3. Likes Endpoints

| HTTP Method | Endpoint | FastAPI Handler | Spring Boot Controller |
|-------------|----------|----------------|----------------------|
| POST | `/api/posts/{postId}/likes` | `like_post_endpoint()` | `LikeController.likePost()` |
| DELETE | `/api/posts/{postId}/likes` | `unlike_post_endpoint()` | `LikeController.unlikePost()` |

**Kết luận:** Tất cả 12 endpoints đã được migration hoàn toàn với cấu trúc và chức năng giống hệt nhau.

---

## 8. DATABASE SCHEMA

### 8.1. Posts Table
```sql
CREATE TABLE posts (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
```

### 8.2. Comments Table
```sql
CREATE TABLE comments (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
)
```

### 8.3. Likes Table
```sql
CREATE TABLE likes (
    post_id TEXT NOT NULL,
    username TEXT NOT NULL,
    liked_at TEXT NOT NULL,
    PRIMARY KEY (post_id, username),
    FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
)
```

### 8.4. Relationships
- **One Post → Many Comments** (1-to-many)
- **One Post → Many Likes** (1-to-many)
- Cascade delete: Khi xóa post, tự động xóa comments và likes liên quan

---

## 9. TESTING VÀ VALIDATION

### 9.1. Test Cases đã thực hiện

#### 9.1.1. Post Management Tests
- ✅ GET `/api/posts` - Trả về empty array khi database mới
- ✅ POST `/api/posts` - Tạo post thành công với valid data
- ✅ POST `/api/posts` - Trả về 400 khi missing required fields
- ✅ GET `/api/posts/{postId}` - Trả về post details
- ✅ GET `/api/posts/{postId}` - Trả về 404 khi post không tồn tại
- ✅ PATCH `/api/posts/{postId}` - Update post thành công
- ✅ DELETE `/api/posts/{postId}` - Xóa post thành công (204)

#### 9.1.2. Comment Management Tests
- ✅ GET `/api/posts/{postId}/comments` - Liệt kê comments
- ✅ POST `/api/posts/{postId}/comments` - Tạo comment thành công
- ✅ Cascade delete - Comments bị xóa khi post bị xóa

#### 9.1.3. Like System Tests
- ✅ POST `/api/posts/{postId}/likes` - Like post thành công
- ✅ DELETE `/api/posts/{postId}/likes` - Unlike post thành công
- ✅ Duplicate like prevention - Không thể like 2 lần

### 9.2. OpenAPI/Swagger UI Validation
- ✅ Swagger UI accessible tại `http://localhost:8080/swagger-ui.html`
- ✅ OpenAPI JSON accessible tại `http://localhost:8080/openapi.json`
- ✅ API documentation matches openapi.yaml specification
- ✅ Các tags được group đúng: Posts, Comments, Likes

### 9.3. Database Validation
- ✅ Database file `sns_api.db` được tạo tự động
- ✅ Tables được khởi tạo lại mỗi lần restart app
- ✅ Foreign key constraints hoạt động đúng
- ✅ UUID generation cho IDs

---

## 10. CHALLENGES VÀ GIẢI PHÁP

### 10.1. Challenge 1: SQLite với Spring Data JPA
**Vấn đề:** Spring Boot không hỗ trợ SQLite dialect mặc định

**Giải pháp:**
- Thêm dependency `hibernate-community-dialects`
- Cấu hình `spring.jpa.database-platform=org.hibernate.community.dialect.SQLiteDialect`

### 10.2. Challenge 2: Database Initialization
**Vấn đề:** Cần reinitialize database mỗi lần start app

**Giải pháp:**
- Sử dụng `@PostConstruct` trong DatabaseConfig
- Execute DROP TABLE trước CREATE TABLE
- Sử dụng `JdbcTemplate` để run raw SQL

### 10.3. Challenge 3: Matching OpenAPI Specification Exactly
**Vấn đề:** Đảm bảo generated OpenAPI doc giống hệt openapi.yaml

**Giải pháp:**
- Cấu hình OpenApiConfig với info, servers, contact matching
- Sử dụng SpringDoc annotations: @Operation, @Tag
- Custom application.properties cho springdoc paths

### 10.4. Challenge 4: String-based Timestamps
**Vấn đề:** FastAPI sử dụng ISO-8601 string cho timestamps, không phải Date objects

**Giải pháp:**
- Entity fields dùng `String` thay vì `LocalDateTime`
- Generate từ `Instant.now().toString()` để match format

### 10.5. Challenge 5: Composite Primary Key cho Likes
**Vấn đề:** Likes table có composite PK (post_id, username)

**Giải pháp:**
- Tạo `@Embeddable` class `LikeId`
- Sử dụng `@EmbeddedId` trong Like entity
- Implement `equals()` và `hashCode()` đúng cách

---

## 11. BEST PRACTICES ĐÃ ÁP DỤNG

### 11.1. Spring Boot Best Practices
- ✅ Layered architecture: Controller → Service → Repository
- ✅ DTOs riêng biệt cho Request và Response
- ✅ Constructor injection thay vì field injection
- ✅ @RequiredArgsConstructor với Lombok
- ✅ Global exception handling với @ControllerAdvice
- ✅ RESTful API design patterns
- ✅ Proper HTTP status codes

### 11.2. Java Code Quality
- ✅ Lombok để reduce boilerplate code
- ✅ Meaningful class và method names
- ✅ JavaDoc comments cho public methods
- ✅ Consistent code formatting
- ✅ SOLID principles

### 11.3. Database Best Practices
- ✅ JPA entities với proper annotations
- ✅ Foreign key constraints
- ✅ Cascade operations
- ✅ Index on primary keys
- ✅ NOT NULL constraints cho required fields

### 11.4. API Documentation
- ✅ OpenAPI 3.0 specification
- ✅ Clear operation summaries và descriptions
- ✅ Tag grouping cho endpoints
- ✅ Swagger UI cho interactive testing

---

## 12. KẾT QUẢ ĐẠT ĐƯỢC

### 12.1. Checklist hoàn thành ✅

- [x] **Migration hoàn toàn tất cả endpoints**
  - 5 Post endpoints
  - 5 Comment endpoints
  - 2 Like endpoints
  
- [x] **Database configuration**
  - SQLite database: `sns_api.db`
  - Auto-initialization on startup
  - 3 tables với proper relationships
  
- [x] **OpenAPI và Swagger UI**
  - Swagger UI tại `/swagger-ui.html`
  - OpenAPI JSON tại `/openapi.json`
  - Matches openapi.yaml specification
  
- [x] **Code quality**
  - Layered architecture
  - DTOs cho request/response
  - Exception handling
  - Validation
  
- [x] **Testing**
  - All endpoints tested và working
  - Error cases handled properly

### 12.2. Metrics

| Metric | Value |
|--------|-------|
| Total Java Classes | ~25 classes |
| Total Endpoints | 12 endpoints |
| Lines of Code (LOC) | ~1500 lines |
| Dependencies | 7 main dependencies |
| Build Time | ~10 seconds |
| Startup Time | ~3-4 seconds |

### 12.3. Project Structure Quality

```
✅ Clear package structure
✅ Separation of concerns
✅ Single Responsibility Principle
✅ Dependency Injection
✅ Configuration externalization
```

---

## 13. HƯỚNG PHÁT TRIỂN TRONG TƯƠNG LAI

### 13.1. Improvements có thể thực hiện

1. **Security**
   - Thêm Spring Security
   - JWT authentication
   - Role-based access control (RBAC)

2. **Database**
   - Migrate từ SQLite sang PostgreSQL/MySQL cho production
   - Add database migrations với Flyway/Liquibase
   - Implement connection pooling

3. **Testing**
   - Unit tests với JUnit 5 và Mockito
   - Integration tests với @SpringBootTest
   - API tests với MockMvc hoặc RestAssured

4. **Performance**
   - Add caching với Spring Cache
   - Implement pagination cho list endpoints
   - Database query optimization

5. **Monitoring**
   - Spring Boot Actuator endpoints
   - Logging với SLF4J và Logback
   - Application metrics với Micrometer

6. **Containerization**
   - Dockerfile cho Spring Boot app
   - Docker Compose cho full stack
   - Kubernetes deployment manifests

---

## 14. KẾT LUẬN

### 14.1. Tóm tắt

Dự án đã thành công trong việc migration một ứng dụng Social Media API từ Python FastAPI sang Java Spring Boot, đảm bảo:

- ✅ **100% tương thích về chức năng** - Tất cả endpoints hoạt động giống hệt
- ✅ **Đúng OpenAPI specification** - API document matches openapi.yaml
- ✅ **Clean Architecture** - Áp dụng best practices của Spring Boot
- ✅ **Database consistency** - SQLite với auto-initialization
- ✅ **Documentation** - Swagger UI và OpenAPI JSON

### 14.2. Kinh nghiệm học được

1. **Framework Migration Skills:**
   - Hiểu sâu về FastAPI và Spring Boot
   - Mapping concepts giữa Python và Java
   - Adapter design pattern trong practice

2. **Spring Boot Expertise:**
   - Spring Data JPA và Hibernate
   - RESTful API development
   - OpenAPI integration
   - Configuration management

3. **Problem Solving:**
   - SQLite integration với Spring Boot
   - Database initialization strategies
   - OpenAPI specification compliance

4. **Best Practices:**
   - Clean Code principles
   - SOLID principles
   - RESTful API design
   - Layered architecture

### 14.3. Ứng dụng thực tế

Migration này minh họa kỹ năng quan trọng trong software engineering:
- **Legacy system modernization**
- **Technology stack migration**
- **Multi-language development**
- **API-first design**

Những kỹ năng này rất có giá trị trong môi trường enterprise, nơi việc migrate giữa các technologies là phổ biến.

---

## 15. TÀI LIỆU THAM KHẢO

### 15.1. Documentation
- [Spring Boot Official Documentation](https://spring.io/projects/spring-boot)
- [Spring Data JPA Reference](https://spring.io/projects/spring-data-jpa)
- [SpringDoc OpenAPI Documentation](https://springdoc.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification 3.0](https://swagger.io/specification/)

### 15.2. Tools Used
- **GitHub Copilot** - AI code completion và suggestions
- **Context7 MCP Server** - Documentation lookup
- **IntelliJ IDEA / VS Code** - IDE
- **Postman** - API testing
- **Gradle** - Build tool

### 15.3. Libraries & Frameworks
- Spring Boot 3.5.0
- Spring Data JPA
- Hibernate Community Dialects
- SpringDoc OpenAPI 2.7.0
- SQLite JDBC 3.47.1.0
- Lombok
- Jakarta Validation

---

## PHỤ LỤC

### A. Cách chạy ứng dụng

#### FastAPI (Python)
```bash
cd python
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Spring Boot (Java)
```bash
cd java/socialapp
./gradlew bootRun
```

Hoặc build và run JAR:
```bash
./gradlew build
java -jar build/libs/socialapp-0.0.1-SNAPSHOT.jar
```

### B. Test Endpoints

**Create a post:**
```bash
curl -X POST http://localhost:8080/api/posts \
  -H "Content-Type: application/json" \
  -d '{"username":"john","content":"Hello World!"}'
```

**Get all posts:**
```bash
curl http://localhost:8080/api/posts
```

**Access Swagger UI:**
```
http://localhost:8080/swagger-ui.html
```

### C. Project Statistics

```
Total Files: ~60 files (Java, configs, build files)
Total Lines: ~2000 lines (excluding dependencies)
Packages: 7 main packages
Classes: ~25 classes
Interfaces: 3 (Repositories)
Enums: 0
Tests: Basic structure ready
```

---

**Ngày hoàn thành báo cáo:** 12/02/2026  
**Phiên bản:** 1.0

---

**CHỮ KÝ XÁC NHẬN**

Sinh viên thực hiện: ___________________  
Ngày: ___________________

Giảng viên hướng dẫn: ___________________  
Ngày: ___________________
