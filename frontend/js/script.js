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
            convertBtn.innerHTML = '<span class="spinner"></span><span>변환 중...</span>';
            convertedText.innerHTML = 'AI가 열심히 변환 중입니다...';
            convertedText.classList.add('text-slate-300', 'animate-pulse', 'italic');
            convertedText.classList.remove('text-slate-700');
            copyBtn.disabled = true;
            feedbackSection.classList.add('hidden');
        } else {
            convertBtn.disabled = false;
            convertBtn.innerHTML = '<span>변환하기</span>';
        }
    }

    function displayError(message) {
        convertedText.classList.remove('text-slate-300', 'animate-pulse', 'italic');
        convertedText.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full text-center p-6 bg-red-50 rounded-xl border border-red-100">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-red-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <p class="text-red-800 font-semibold mb-1">오류가 발생했습니다</p>
                <p class="text-red-600 text-sm mb-4">${message}</p>
                <button id="retry-btn" class="btn-primary bg-red-600 hover:bg-red-700">다시 시도</button>
            </div>
        `;
        document.getElementById('retry-btn').addEventListener('click', handleConvert);
    }

    // 결과 표시 함수
    function displayResult(text) {
        convertedText.textContent = text;
        convertedText.classList.remove('text-slate-300', 'animate-pulse', 'italic');
        convertedText.classList.add('text-slate-700');
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
        const toastMsg = document.getElementById('toast-message');
        if (toastMsg) toastMsg.textContent = message;
        
        toast.classList.remove('hidden');
        // Wait for a frame to ensure the 'hidden' removal is processed before adding transition classes
        requestAnimationFrame(() => {
            toast.classList.remove('opacity-0', 'translate-y-4');
            toast.classList.add('opacity-100', 'translate-y-0');
        });
        
        setTimeout(() => {
            toast.classList.remove('opacity-100', 'translate-y-0');
            toast.classList.add('opacity-0', 'translate-y-4');
            
            // Wait for transition to finish before adding hidden back
            setTimeout(() => {
                toast.classList.add('hidden');
            }, 300);
        }, 3000);
    }
});
