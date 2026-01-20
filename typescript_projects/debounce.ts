type genericFunc = (...args: any[]) => void

/**
 * Debouce function allows you to save multiple calls to an API in a very short duration on user's action.
 * Example: A u  */
function debounce<T extends genericFunc> (fn: T, delay): (...args: Parameters<T>) => void {
    let timer: ReturnType<typeof setTimeout> | null = null

    return function(...args: Parameters<T>) {
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => {
            fn.apply(this, args)
        }, delay)
    }
}