package main

import (
	"fmt"
	"io/ioutil"
	"math/rand"
	"path/filepath"
)

func readSudoku(filename string) ([][]byte, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	grid := group(filter(data), 9)
	return grid, nil
}

func filter(values []byte) []byte {
	filteredValues := make([]byte, 0)
	for _, v := range values {
		if (v >= '1' && v <= '9') || v == '.' {
			filteredValues = append(filteredValues, v)
		}
	}
	return filteredValues
}

func display(grid [][]byte) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
			fmt.Print(string(grid[i][j]))
		}
		fmt.Println()
	}
}

func group(values []byte, n int) [][]byte {
	result := make([][]byte, 0, n)
	valNumber := len(values) / n
	for i := 0; i < valNumber; i++ {
		row := make([]byte, n)
		for j := 0; j < n; j++ {
			row[j] = byte(values[n*i+j])
		}
		result = append(result, row)
	}
	return result
}

func getRow(grid [][]byte, row int) []byte {
	return grid[row]
}

func getCol(grid [][]byte, col int) []byte {
	var result []byte
	for i := 0; i < len(grid); i++ {
		result = append(result, grid[i][col])
	}
	return result
}

func getBlock(grid [][]byte, row int, col int) []byte {
	var result []byte
	blockRow := (row / 3) * 3
	blockCol := (col / 3) * 3
	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			result = append(result, grid[blockRow+i][blockCol+j])
		}
	}
	return result
}

func findEmptyPosition(grid [][]byte) (int, int) {
	for row := 0; row < len(grid); row++ {
		for col := 0; col < len(grid[0]); col++ {
			if grid[row][col] == '.' {
				return row, col
			}
		}
	}
	return -1, -1
}

func contains(values []byte, search byte) bool {
	for _, v := range values {
		if v == search {
			return true
		}
	}
	return false
}

func findPossibleValues(grid [][]byte, row int, col int) []byte {
	var used = make(map[byte]bool)
	block := getBlock(grid, row, col)
	for i := 0; i < len(block); i++ {
		used[block[i]] = true
	}
	rows := getRow(grid, row)
	for i := 0; i < len(rows); i++ {
		used[rows[i]] = true
	}
	cols := getCol(grid, col)
	for i := 0; i < len(cols); i++ {
		used[cols[i]] = true
	}
	var isNotValid bool
	counter := 0
	for i := 49; i < 58; i++ {
		_, isNotValid = used[byte(i)]
		if !isNotValid {
			counter++
		}
	}
	result := make([]byte, counter)
	counter = 0
	for i := 49; i < 58; i++ {
		_, isNotValid = used[byte(i)]
		if !isNotValid {
			result[counter] = byte(i)
			counter++
		}
	}
	return result
}

func solve(grid [][]byte) ([][]byte, bool) {
	row, col := findEmptyPosition(grid)
	if row != -1 {
		result := findPossibleValues(grid, row, col)
		for _, val := range result {
			grid[row][col] = byte(val)
			solution, status := solve(grid)
			if status {
				return solution, true
			}
			grid[row][col] = '.'
		}
	} else {
		return grid, true
	}
	return grid, false
}

func checkSolution(grid [][]byte) bool {
	for col := 0; col < 9; col++ {
		colVals := getCol(grid, col)
		result := make(map[int]bool)
		count := 0
		for val := range colVals {
			if val == '.' {
				return false
			}
			if result[val] == false {
				result[val] = true
				count++
			}
		}
		if count != 9 {
			return false
		}
	}
	return true
}

func generateSudoku(N int) [][]byte {
	var grid [][]byte
	indexes := make(map[int][]byte)
	for i := byte(0); i < 9; i++ {
		for j := byte(0); j < 9; j++ {
			grid[i][j] = '.'
			indexes[int(9*i+j)] = append(indexes[int(9*i+j)], i)
			indexes[int(9*i+j)] = append(indexes[int(9*i+j)], j)
		}
	}
	grid, _ = solve(grid)
	N = 81 - N
	for i := 0; i < 81-N; i++ {
		num := rand.Intn(len(indexes) - 1)
		row, col := indexes[num][0], indexes[num][1]
		grid[row][col] = '.'
		delete(indexes, num)
	}
	return grid
}

func main() {
	puzzles, err := filepath.Glob("puzzle*.txt")
	if err != nil {
		fmt.Printf("Could not find any puzzles")
		return
	}
	for _, fname := range puzzles {
		go func(fname string) {
			grid, _ := readSudoku(fname)
			solution, _ := solve(grid)
			fmt.Println("Solution for", fname)
			display(solution)
		}(fname)
	}
	var input string
	fmt.Scanln(&input)
}
