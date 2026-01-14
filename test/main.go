// package main

// // file: models/book.go
// type Book struct {
//     ID string `json: "id"`
//     Title string `json: "title"`
//     Author string `json: "author"`
//     Count int `json: `
// }

// // file: models/user.go
// type User struct {
//     ID string `json: "id"`
//     Name string `json: "name"`
// }

// // file: book_store.go
// package main
// import "sync"

// var bookStore = make(map[string]int)
// var bsMu sync.RWMutex

// //file: request_handlers.go
// package main
// import {
//     "github.com/gin-gonic/gin"
// }

// func postBook(ctx *gin.Context) 
// {
//     var book Book
//     ctx, cancel := context.WithTimeout(c.Request.conte)
//     if err := c.ShouldBindJSON(&book); err != nil {
//         c.JSON(http.StatusBadRequest, )
//         return
//     }

//     if book.ID == "" || book.Title == "" {
//         c.JSON(http.StatusBadRequest, )
//         return
//     }
//     bsMu.Lock()
//     val, ok := bookStore[book.ID]
//     if !ok {
//         bookStore[book.ID] = 1
//     }
//     else {
//         bookStore[book.ID] += 1
//     }
//     bsMu.unLock()
//     c.JSON(http.StatusCreated, book)
// }

// //file: auth.go
// // Auth Service
// package main
// import (
//     "strings"
//     "github.com/gin-gonic/gin"
// )

// func authMiddleware() gin.Handlerfunc {
//     return func(c *gin.Context) {
//         auth := c.GetHeader("Authorization")
//         if strings.Hasprefix(auth, "Bearer ") {
//             c.JSON(
//                 http.StatusUnauthorized
//                 gin.H{"error": "Invalid Auth token"}
//             )
//         }
//         user, ok := UnmarshalAuthToke(auth)
//         if !ok {
//             c.JSON(
//                 http.Forbidden,
//                 gin.H{"error": "Forbidden, Invalid Auth token"}
//             )
//         }
//         db = db.WithContext(c)
//     }
// }


package main

import (
    "sync"
)

func process(i int, wg *sync.WaitGroup, ch chan int){
    defer wg.Done()

    ch <- i
    fmt.Println("processing ith process", i)

    <- ch
}
func main() {
    var wg sync.WaitGroup

    totalProcesses:= 10
    maxConcurrent := 3

    ch := make(chan int, maxConcurrent)

    for i:= 1; i<=totalProcesses; i++ {
        wg.Add(1)
        go process(i, &wg, ch)
    }

    wg.Wait()
    fmt.Println("All process completed")
}
