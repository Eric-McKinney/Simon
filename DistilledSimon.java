package SimonGame;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;
import java.io.IOException;

public class DistilledSimon {

	public static void clear() {
		for (int i = 0; i < 80; i++) {
			System.out.println();
		}
	}
	
	public static void saveScore(int score) {
		File file = new File("java_high_score.txt");
		
		try {
			file.createNewFile();
			FileWriter writer = new FileWriter("java_high_score.txt");
			String scoreString = Integer.toString(score);
			
			writer.write(scoreString);
			writer.close();
			
		} catch (IOException e) {
			System.out.println("An error has occurred in saveScore");
			e.printStackTrace();
		}
	}
	
	public static String getRandomColor() {
		String[] colors = {"green", "red", "yellow", "blue"};
		Random random = new Random();
		int randIdx = random.nextInt(colors.length);
		String randColor = colors[randIdx];
		return randColor;
	}
	
	public static void gameOver(int score) {
		int highScore;
		try {
			File file = new File("java_high_score.txt");
			Scanner reader = new Scanner(file);
			highScore = reader.nextInt();
			reader.close();
		} catch (FileNotFoundException e) {
			saveScore(score);
			highScore = score;
		}
		
		if (score > highScore) {
			saveScore(score);
			highScore = score;
		}
		
		System.out.println("Game Over\nScore = " + score + "\nHigh Score = " 
							+ highScore);
	}
	
	public static void printSequence(ArrayList<String> sequence) {
		for (int idx = 0; idx < sequence.size(); idx++) {
			System.out.println(sequence.get(idx));
			
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				System.out.println("Error in printSequence");
				e.printStackTrace();
			}
			
			clear();
		}
	}
	
	public static int guessSequence(ArrayList<String> sequence, int score, Scanner scanner) {
		int tempScore = 0;
		String guess;
		
		for (int idx = 0; idx < sequence.size(); idx++) {
			System.out.print("color: ");
			guess = scanner.next().toLowerCase();
			clear();
			
			if (guess.equals(sequence.get(idx))) {
				tempScore++;
				
				if (tempScore > score) {
					score = tempScore;
				}
			} else {
				gameOver(score);
				score = -1; // Trying to end loop in main so make score < 0
				break;
			}
		}
		return score;
	}
	
	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		ArrayList<String> sequence = new ArrayList<String>();
		int score = 0;
		Boolean run = true;
		
		while (run) {
			try {
				Thread.sleep(250);
			} catch (InterruptedException e) {
				System.out.println("Error in main");
				e.printStackTrace();
			}
			
			sequence.add(getRandomColor());
			printSequence(sequence);
			score = guessSequence(sequence, score, scanner);
			
			if (score < 0) { // score set to -1 when game over
				scanner.close();
				break;
			}
		}
	}
}
