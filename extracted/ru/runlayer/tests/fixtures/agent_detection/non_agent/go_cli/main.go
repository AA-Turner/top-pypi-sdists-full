// Plain Gin HTTP CLI — not an AI agent (zero-false-positive fixture).
package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})
	_ = r.Run(":8080")
}
