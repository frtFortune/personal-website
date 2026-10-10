document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('project-form');
    const submitBtn = document.getElementById('submit-btn');
    const toast = document.getElementById('toast');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    function showToast(title, message, type = 'success') {
        toast.classList.remove('hidden', 'bg-emerald-950/50', 'border-emerald-800', 'text-emerald-200', 'bg-rose-950/50', 'border-rose-800', 'text-rose-200');
        
        if (type === 'success') {
            toast.classList.add('bg-emerald-950/50', 'border-emerald-800', 'text-emerald-200');
            toastIcon.innerHTML = `<svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>`;
        } else {
            toast.classList.add('bg-rose-950/50', 'border-rose-800', 'text-rose-200');
            toastIcon.innerHTML = `<svg class="w-5 h-5 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>`;
        }

        toastTitle.textContent = title;
        toastMessage.textContent = message;
        toast.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const apiUrl = document.getElementById('api-url').value.trim().replace(/\/+$/, '');
        const apiKey = document.getElementById('api-key').value.trim();
        const title = document.getElementById('title').value.trim();
        const description = document.getElementById('description').value.trim();
        const rawTags = document.getElementById('tags').value.trim();
        const demoUrl = document.getElementById('demo-url').value.trim() || '#';
        const githubUrl = document.getElementById('github-url').value.trim() || '#';

        const tagsArray = rawTags.split(',').map(tag => tag.trim()).filter(Boolean);

        if (tagsArray.length === 0) {
            showToast('Validation Error', 'Please provide at least one valid tag.', 'error');
            return;
        }

        const payload = {
            title: title,
            description: description,
            tags: tagsArray,
            demo_url: demoUrl,
            github_url: githubUrl
        };

        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Publishing...
        `;

        try {
            const response = await fetch(`${apiUrl}/api/projects`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': apiKey
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || `Server returned status ${response.status}`);
            }

            showToast('Success!', `Project "${data.project.title}" was successfully created with ID #${data.project.id}!`, 'success');
            form.reset();
            document.getElementById('api-url').value = apiUrl;
        } catch (error) {
            showToast('Failed to Publish', error.message || 'An unexpected network error occurred.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `
                <span>Publish Project</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                </svg>
            `;
        }
    });
});