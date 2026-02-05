# GEMINI.md - BizTone Converter 프로젝트 컨텍스트

## 프로젝트 개요
**BizTone Converter**는 일상적인 언어를 전문적인 비즈니스 언어로 변환해주는 AI 기반 웹 애플리케이션입니다. 주요 타겟 수신자는 다음과 같습니다:
- **상사 (Upward):** 격식 있고 간결한 보고 스타일.
- **동료 (Lateral):** 존중하고 협력적인 톤.
- **고객 (External):** 매우 정중하고 서비스 지향적인 언어.

본 프로젝트는 **Flask** 백엔드를 사용하여 **Groq AI API**(`llama-3.3-70b-versatile` 모델)와 통신하며, 현대적인 **Tailwind CSS**로 스타일링된 프론트엔드를 제공합니다.

## 프로젝트 구조
- `backend/`: Flask 서버(`app.py`) 및 의존성 파일(`requirements.txt`) 포함.
- `frontend/`: 사용자 인터페이스 파일(`index.html`, `css/style.css`, `js/script.js`) 포함.
- `PRD.md`: 상세 제품 요구사항 문서.
- `프로그램개요서.md`: 프로젝트 개요 및 시스템 아키텍처 문서.
- `my-rules.md`: Gemini CLI를 위한 사용자 정의 행동 지침.

## 빌드 및 실행 방법

### 사전 요구사항
- Python 3.11 이상.
- Groq API 키.

### 설정 및 실행 순서
1.  **가상 환경 설정:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Unix/macOS
    source .venv/bin/activate
    ```
2.  **의존성 설치:**
    ```bash
    pip install -r backend/requirements.txt
    ```
3.  **환경 변수 설정:**
    루트 디렉토리에 `.env` 파일을 생성하고 API 키를 추가합니다:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```
4.  **애플리케이션 실행:**
    ```bash
    python backend/app.py
    ```
    브라우저에서 `http://localhost:5000` 접속.

## 개발 컨벤션

### 코딩 스타일 및 표준
- **백엔드:** 라우팅 및 API 엔드포인트 처리를 위해 Flask 사용. Python 표준(PEP 8) 준수.
- **프론트엔드:** 스타일링을 위해 Tailwind CSS(Play CDN) 사용. 둥근 모서리(`rounded-2xl`)와 부드러운 그림자를 활용한 "Smooth" UI 지향.
- **AI 로직:** `backend/app.py`에 정의된 시스템 프롬프트를 통해 수신자별 맞춤형 변환 수행.
- **통신:** 프론트엔드와 백엔드 간의 비동기 통신을 위해 Fetch API 사용.

### 참고용 주요 파일
- `backend/app.py`: AI 변환 로직 및 정적 파일 서빙의 핵심.
- `frontend/js/script.js`: UI 상호작용, API 호출 및 상태 관리(로딩, 에러, 성공) 담당.
- `PRD.md`: 기능 및 프로젝트 목표에 대한 단일 진실 공급원(SSOT).

### Git 가이드라인
- 커밋 메시지는 명확해야 하며 일관된 형식을 따릅니다 (예: `feat:`, `ui:`, `refactor:`, `fix:`).
- **중요:** `.env` 파일이나 로그 파일은 커밋하지 않습니다.

## Gemini CLI 사용 지침
- `my-rules.md`의 지침을 엄격히 준수하십시오.
- 코드를 수정할 때는 기존 Tailwind CSS 스타일 및 프로젝트 구조와의 일관성을 유지하십시오.
- `PRD.md`에 정의된 목표에 따라 테스트나 개선 사항을 능동적으로 제안하십시오.