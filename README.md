-----

##  랩가드 (LabGuard)

랩가드는 **연구실 안전 관리 및 비품/시약 재고 관리를 위한 통합 웹 애플리케이션**입니다. 연구실 내의 잠재적 위험 요소를 관리하고, 비품 및 시약의 효율적인 재고 파악 및 사용 이력을 추적하여 안전하고 체계적인 연구 환경을 조성하는 데 기여합니다.

-----

###  주요 기능

  * **위험 물질 관리**:
      * 화학 물질, 고압 가스 등 위험 물질의 종류, 보관 위치, 유해성 정보 등록 및 조회.
      * 물질안전보건자료(MSDS) 첨부 및 열람 기능.
      * 유통기한 임박 알림 및 폐기 예정 물질 관리.
  * **비품 및 시약 재고 관리**:
      * 비품 및 시약의 입고/출고, 재고 현황 실시간 파악.
      * 바코드/QR 코드 스캔을 통한 간편한 입출고 처리.
      * 최소 재고량 설정 및 부족 시 알림 기능.
      * 사용자별 사용 이력 추적.
  * **안전 교육 및 공지**:
      * 필수 안전 교육 자료 업로드 및 교육 이수 현황 관리.
      * 연구실 안전 수칙 및 공지사항 게시판.
      * 비상 연락망 및 비상 상황 발생 시 대처 요령 안내.
  * **사고 및 재해 보고**:
      * 연구실 내 사고 발생 시 간편한 보고 시스템.
      * 사고 유형, 경위, 피해 정도 등 상세 기록 및 분석.
      * 재발 방지 대책 수립 지원.
  * **사용자 및 권한 관리**:
      * 연구원, 관리자 등 사용자 역할별 접근 권한 설정.
      * 각 사용자의 활동 기록 로깅.

-----

###  기술 스택

  * **Frontend**: React, Next.js
  * **Backend**: Python, Django / Django REST Framework
  * **Database**: PostgreSQL
  * **Deployment**: Docker, AWS (예: EC2, S3, RDS)

-----

### 🛠 설치 및 실행 방법

1.  **리포지토리 클론**:

    ```bash
    git clone https://github.com/your-username/labguard.git
    cd labguard
    ```

2.  **환경 설정**:
    프로젝트 루트에 `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다. (예: 데이터베이스 연결 정보 등)

    ```
    # .env 예시
    DATABASE_URL="postgresql://user:password@host:port/database"
    SECRET_KEY="your-django-secret-key"
    # 기타 필요한 환경 변수
    ```

3.  **의존성 설치**:

      * **Backend (Python)**:
        ```bash
        pip install -r requirements.txt
        ```
      * **Frontend (Node.js)**:
        ```bash
        npm install
        # 또는 yarn install
        ```

4.  **데이터베이스 마이그레이션 (Backend)**:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **애플리케이션 실행**:

      * **Backend**:
        ```bash
        python manage.py runserver
        ```
      * **Frontend**:
        ```bash
        npm run dev
        # 또는 yarn dev
        ```

6.  **접속**:
    브라우저에서 `http://localhost:3000` (프론트엔드)에 접속하여 랩가드를 시작합니다. 백엔드 API는 `http://localhost:8000` 에서 실행됩니다.

-----

# LabGuard_Proj 폴더 구조

```
LabGuard_Proj/
├── main.py                # FastAPI 앱 진입점
├── requirements.txt       # 의존성 목록
├── .env                   # 환경변수 파일
├── README.md              # 프로젝트 설명 및 구조
app/
│   main.py
├── api/
│   └── ..._router.py    # FastAPI 엔드포인트(라우터)
├── services/
│   └── ..._service.py   # 비즈니스 로직 (DB/AI/처리 등)
├── schemas/
│   └── ...py            # Pydantic 데이터 모델(요청/응답)
├── db/
│   └── ...py            # DB 연결/ORM 등
└── core/
    └── ...py            # 공통 유틸, 설정 등
