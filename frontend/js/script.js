document.addEventListener('DOMContentLoaded', () => {
    const originalText = document.getElementById('original-text');
    const targetAudience = document.getElementById('target-audience');
    const convertBtn = document.getElementById('convert-btn');
    const convertedText = document.getElementById('converted-text');
    const charCount = document.getElementById('char-count');
    const copyBtn = document.getElementById('copy-btn');
    const clearBtn = document.getElementById('clear-btn');
    const feedbackSection = document.getElementById('feedback-section');
    const toast = document.getElementById('toast');

    // API URL - 상대 경로 사용
    const API_URL = '/api/convert';

    // 입력창 이벤트 처리
    originalText.addEventListener('input', () => {
        const length = originalText.value.length;
        charCount.textContent = `${length} / 500`;
        
        // 지우기 버튼 표시 여부
        if (length > 0) {
            clearBtn.classList.remove('hidden');
            convertBtn.disabled = false;
        } else {
            clearBtn.classList.add('hidden');
            convertBtn.disabled = true;
        }
    });

    // 지우기 버튼 클릭
    clearBtn.addEventListener('click', () => {
        originalText.value = '';
        originalText.dispatchEvent(new Event('input'));
        originalText.focus();
    });

    // 변환 버튼 클릭 이벤트
    convertBtn.addEventListener('click', handleConvert);

    async function handleConvert() {
        const text = originalText.value.trim();
        const target = targetAudience.value;

        if (!text) return;

        // 로딩 상태 표시
        setLoading(true);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text, target }),
            });

            if (!response.ok) {
                throw new Error('서버와 통신 중 문제가 발생했습니다.');
            }

            const data = await response.json();
            
            // 결과 표시
            displayResult(data.converted);
            
            // UI 상태 업데이트
            copyBtn.disabled = false;
            feedbackSection.classList.remove('hidden');
        } catch (error) {
            console.error('Error:', error);
            displayError(error.message);
        } finally {
            setLoading(false);
        }
    }

    function setLoading(isLoading) {
        if (isLoading) {
            convertBtn.disabled = true;
            convertBtn.innerHTML = '<span class="spinner"></span>변환 중...';
            convertedText.innerHTML = '<p class="placeholder-text">AI가 열심히 변환 중입니다...</p>';
            copyBtn.disabled = true;
            feedbackSection.classList.add('hidden');
        } else {
            convertBtn.disabled = false;
            convertBtn.textContent = '변환하기';
        }
    }

    function displayError(message) {
        convertedText.innerHTML = `
            <div class="error-container">
                <p>오류가 발생했습니다: ${message}</p>
                <p>잠시 후 다시 시도해주세요.</p>
                <button id="retry-btn" class="primary-btn retry-btn">다시 시도</button>
            </div>
        `;
        document.getElementById('retry-btn').addEventListener('click', handleConvert);
    }

    // 결과 표시 함수
    function displayResult(text) {
        // 줄바꿈 보존을 위해 pre-wrap 스타일이 적용된 div에 텍스트 삽입
        convertedText.textContent = text;
    }

    // 복사하기 버튼 클릭 이벤트
    copyBtn.addEventListener('click', () => {
        const text = convertedText.textContent;
        if (!text) return;

        navigator.clipboard.writeText(text).then(() => {
            showToast('복사되었습니다!');
        }).catch(err => {
            console.error('복사 실패:', err);
            showToast('복사에 실패했습니다.');
        });
    });

    // 피드백 버튼 클릭 이벤트
    document.querySelectorAll('.feedback-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const type = btn.getAttribute('data-type');
            showToast('피드백이 전달되었습니다. 감사합니다!');
            feedbackSection.classList.add('hidden');
        });
    });

    // 토스트 알림 표시 함수
    function showToast(message) {
        toast.textContent = message;
        toast.classList.remove('hidden');
        
        setTimeout(() => {
            toast.classList.add('hidden');
        }, 2000);
    }
});
