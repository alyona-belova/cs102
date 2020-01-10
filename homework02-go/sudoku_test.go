package main

import (
	"bytes"
	"reflect"
	"testing"
)

func TestGroup(t *testing.T) {
	result := group([]byte{1, 2, 3, 4}, 2)
	expectedResult := [][]byte{{1, 2}, {3, 4}}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}

	result = group([]byte{1, 2, 3, 4, 5, 6, 7, 8, 9}, 3)
	expectedResult = [][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}
}

func TestGetCol(t *testing.T) {
	result := getCol([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 0)
	expectedResult := []byte{1, 4, 7}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}

	result = getCol([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 1)
	expectedResult = []byte{2, 5, 8}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}

	result = getCol([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 2)
	expectedResult = []byte{3, 6, 9}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}
}

func TestGetRow(t *testing.T) {
	result := getRow([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 0)
	expectedResult := []byte{1, 2, 3}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}

	result = getRow([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 1)
	expectedResult = []byte{4, 5, 6}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}

	result = getRow([][]byte{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, 2)
	expectedResult = []byte{7, 8, 9}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}
}

func TestGetBlock(t *testing.T) {
	grid, _ := readSudoku("puzzle1.txt")
	result := getBlock(grid, 0, 1)
	expectedResult := []byte{'5', '3', '.', '6', '.', '.', '.', '9', '8'}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}

	result = getBlock(grid, 4, 7)
	expectedResult = []byte{'.', '.', '3', '.', '.', '1', '.', '.', '6'}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}

	result = getBlock(grid, 8, 8)
	expectedResult = []byte{'2', '8', '.', '.', '.', '5', '.', '7', '9'}
	if !reflect.DeepEqual(result, expectedResult) {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}
}

func TestFindEmptyPosition(t *testing.T) {
	row, col := findEmptyPosition([][]byte{{1, 2, '.'}, {4, 5, 6}, {7, 8, 9}})
	expectedRow, expectedCol := 0, 2
	if row != expectedRow || col != expectedCol {
		t.Fatalf("Expected '(%d,%d)' but got '(%d,%d)'",
			expectedRow, expectedCol, row, col)
	}

	row, col = findEmptyPosition([][]byte{{1, 2, 3}, {4, '.', 6}, {7, 8, 9}})
	expectedRow, expectedCol = 1, 1
	if row != expectedRow || col != expectedCol {
		t.Fatalf("Expected '(%d,%d)' but got '(%d,%d)'",
			expectedRow, expectedCol, row, col)
	}

	row, col = findEmptyPosition([][]byte{{1, 2, 3}, {4, 5, 6}, {'.', 8, 9}})
	expectedRow, expectedCol = 2, 0
	if row != expectedRow || col != expectedCol {
		t.Fatalf("Expected '(%d,%d)' but got '(%d,%d)'",
			expectedRow, expectedCol, row, col)
	}
}

func TestFindPossibleValues(t *testing.T) {
	grid, _ := readSudoku("puzzle1.txt")
	result := findPossibleValues(grid, 0, 2)
	expectedResult := []byte{'1', '2', '4'}

	if bytes.Compare(result, expectedResult) != 0 {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}

	result = findPossibleValues(grid, 4, 7)
	expectedResult = []byte{'2', '5', '9'}
	if bytes.Compare(result, expectedResult) != 0 {
		t.Fatalf("Expected '%v' but got '%v'", expectedResult, result)
	}
}

func TestSolve(t *testing.T) {
	grid, _ := readSudoku("puzzle1.txt")
	solution, _ := solve(grid)
	expectedSolution, _ := readSudoku("puzzle1_solution.txt")
	if !reflect.DeepEqual(solution, expectedSolution) {
		t.Fatalf("Expected '%v' but got '%v'", expectedSolution, solution)
	}
}

func TestCheckSolution(t *testing.T) {
	// TODO: Add test for checkSolution
}

func TestGenerateSudoku(t *testing.T) {
	// TODO: Add test for generateSudoku
}
