import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.util.*;

public class CourierApp {
    private final Scanner input = new Scanner(System.in);
    private final String python = System.getenv().getOrDefault("COURIER_PYTHON", "python");
    private String ask(String label) {
        System.out.print(label + ": ");
        String result = input.nextLine().strip();
        if (result.isEmpty()) throw new IllegalArgumentException("A value is required.");
        return result;
    }
    private void store(String... args) throws Exception {
        var cmd = new ArrayList<>(List.of(python, "store.py"));
        Collections.addAll(cmd, args);
        new ProcessBuilder(cmd).inheritIO().start().waitFor();
    }
    private void book() throws Exception {
        String sender = ask("Sender ID"), receiver = ask("Receiver ID"), kind = ask("Parcel type");
        BigDecimal kg = new BigDecimal(ask("Weight in kg"));
        if (kg.signum() <= 0 || kg.compareTo(new BigDecimal("1000")) > 0)
            throw new IllegalArgumentException("Enter a positive weight up to 1000 kg.");
        String dest = ask("Destination"), zone = ask("Zone (local/regional/national)").toLowerCase(Locale.ROOT);
        int base = switch(zone) {case "local" -> 30; case "regional" -> 60; case "national" -> 100; default -> throw new IllegalArgumentException("Unknown zone.");};
        String service = ask("Service (standard/express)").toLowerCase(Locale.ROOT);
        if (!Set.of("standard","express").contains(service)) throw new IllegalArgumentException("Unknown service.");
        int charge = base + 20 * kg.setScale(0,RoundingMode.CEILING).intValueExact() + (service.equals("express") ? 50 : 0);
        LocalDate booked = LocalDate.now(), due = booked.plusDays(service.equals("express") ? 2 : 5);
        store("book","CP-"+UUID.randomUUID(),sender,receiver,kind,kg.toPlainString(),dest,zone,service,booked.toString(),due.toString(),Integer.toString(charge));
    }
    private void run() throws Exception {
        while (true) {
            System.out.println("\n1 Add customer   2 Add delivery staff   3 List records   4 Book parcel\n5 Assign staff   6 Record movement      7 Record attempt\n8 Track parcel   9 Reports               0 Exit");
            if (!input.hasNextLine()) return;
            try {
                switch (ask("Choice")) {
                    case "0" -> {return;}
                    case "1" -> store("customer",ask("Name"),ask("Phone"),ask("Address"));
                    case "2" -> store("staff",ask("Staff name"));
                    case "3" -> store("list");
                    case "4" -> book();
                    case "5" -> store("assign",ask("Tracking number"),ask("Staff ID"));
                    case "6" -> store("move",ask("Tracking number"),ask("Status (In Transit/Out for Delivery/Returned)"),ask("Location"));
                    case "7" -> {
                        String tracking=ask("Tracking number"), result=ask("Outcome (Delivered/Failed)");
                        store("attempt",tracking,result,result.equals("Failed") ? ask("Failure reason") : "",ask("Location"));
                    }
                    case "8" -> store("history",ask("Tracking number"));
                    case "9" -> store("report");
                    default -> System.out.println("Select 0 to 9.");
                }
            } catch (IllegalArgumentException error) {System.out.println("Rejected: "+error.getMessage());}
            catch (NoSuchElementException end) {return;}
        }
    }
    public static void main(String[] args) throws Exception {new CourierApp().run();}
}
