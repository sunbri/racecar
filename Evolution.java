import java.math.RoundingMode;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

public class Evolution {

    public static void main(String[] args) {
        String text = "The quick brown fox jumps over the lazy dog.";
        new Evolution(text, 1.0 / text.length(), 200);
    }

    private Random random;
    private DecimalFormat df;

    private double mutationRate;
    private int size;
    private int targetLength;
    private int generation = 0;
    private char[] target;
    private char[] parentOne;
    private char[] parentTwo;

    public Evolution (String target, double mutationRate, int size) {
        random = new Random();
        df = new DecimalFormat("0.00");
        df.setRoundingMode(RoundingMode.CEILING);

        this.mutationRate = mutationRate;
        this.size = size;
        this.target = target.toCharArray();

        targetLength = target.length();

        parentOne = new char[targetLength];
        for (int i = 0; i < targetLength; i++) {
            parentOne[i] = randomChar();
        }

        parentTwo = new char[targetLength];
        for (int i = 0; i < targetLength; i++) {
            parentTwo[i] = randomChar();
        }

        System.out.println("Generation: " + generation++ + "  Fitness: " + df.format(hammingDistanceFitness(parentOne, this.target))
            + "  Current: " + new String(parentOne));
        evolve();
    }

    private void evolve() {

        while (true) {

            String[] population = new String[size];
            Double[] fitnessValues = new Double[size];

            for (int i = 0; i < population.length; i++) {
                population[i] = new String(makeChild(parentOne, parentTwo));
                fitnessValues[i] = hammingDistanceFitness(population[i].toCharArray(), target);

            }

            int maxIndex = 0;
            for (int i = 0; i < fitnessValues.length; i++) {
                double fitnessValueNew = fitnessValues[i];
                if (fitnessValueNew >= fitnessValues[maxIndex]) maxIndex = i;
            }

            System.out.println("Generation: " + generation++ + "  Fitness: " + df.format(hammingDistanceFitness(population[maxIndex].toCharArray(), target))
                    + "  Current: " + new String(population[maxIndex].toCharArray()));

            if (fitnessValues[maxIndex] == 1) break;

            int maxIndexTwo = 0;
            ArrayList<Double> fitnessValuesList = new ArrayList<Double>(Arrays.asList(fitnessValues));
            fitnessValuesList.set(maxIndex, 0.0);
            for (int i = 0; i < fitnessValuesList.size(); i++) {
                double fitnessValueNew = fitnessValuesList.get(i);
                if (fitnessValueNew > fitnessValuesList.get(maxIndexTwo)) maxIndexTwo = i;
            }

            parentOne = population[maxIndex].toCharArray();
            parentTwo = population[maxIndexTwo].toCharArray();
        }
    }

    private char[] makeChild(char[] parentOne, char[] parentTwo) {
        char child[] = new char[parentOne.length];
        for (int i = 0; i < child.length; i++) {
            if (random.nextDouble() < mutationRate) {
                child[i] = randomChar();
            } else {
                child[i] = random.nextInt() % 2 == 0 ? parentOne[i] : parentTwo[i];
            }
        }
        return child;
    }

    private double hammingDistanceFitness(char[] string1, char[] string2) {
        int counter = 0;
        for (int i = 0; i < string1.length; i++) {
            if (string1[i] != string2[i]) {
                counter++;
            }
        }
        return 1 - (counter / (1.0 * targetLength));
    }

    private char randomChar() {
        return (char) (32 + random.nextInt(95));
    }
}
