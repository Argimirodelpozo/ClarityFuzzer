(define-data-var count int 0)
(define-data-var hola uint 8)
(define-map counters principal uint)
(define-constant contract-owner tx-sender)
(define-constant neg-one -1)

(define-trait locked-wallet-trait
    (
        (lock (principal uint uint) (response bool uint))
        (bestow (principal) (response bool uint))
        (claim () (response bool uint))
    )
)

(define-read-only (get-counter-value)
    (var-get counter)
)

(define-read-only (add (a uint) (b uint))
    (+ a b)
)