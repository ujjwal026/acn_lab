import java.sql.*;
import java.util.Scanner;

public class jdbc1 {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/testdb";
        String username = "root";
        String password = "";
        Connection connection = null;
        Scanner scanner = new Scanner(System.in);

        try {
            connection = DriverManager.getConnection(url, username, password);
            Statement stmt = connection.createStatement();
            int choice;
            do {
                System.out.println("\nMENU");
                System.out.println("1. Insert User");
                System.out.println("2. View Users");
                System.out.println("3. Update User Age");
                System.out.println("4. Delete User");
                System.out.println("5. Exit");
                System.out.print("Enter your choice: ");
                choice = scanner.nextInt();
                scanner.nextLine(); // Consume newline

                switch (choice) {
                    case 1:
                        System.out.print("Enter name: ");
                        String name = scanner.nextLine();
                        System.out.print("Enter age: ");
                        int age = scanner.nextInt();
                        String insert = "INSERT INTO users (name, age) VALUES ('" + name + "', " + age + ")";
                        stmt.executeUpdate(insert);
                        System.out.println("User added successfully!");
                        break;

                    case 2:
                        String select = "SELECT * FROM users";
                        ResultSet rs = stmt.executeQuery(select);
                        while (rs.next()) {
                            System.out.println("ID: " + rs.getInt("id") + ", Name: " + rs.getString("name") + ", Age: " + rs.getInt("age"));
                        }
                        break;

                    case 3:
                        System.out.print("Enter user ID to update: ");
                        int idToUpdate = scanner.nextInt();
                        System.out.print("Enter new age: ");
                        int newAge = scanner.nextInt();
                        String update = "UPDATE users SET age = " + newAge + " WHERE id = " + idToUpdate;
                        int rowsAffected = stmt.executeUpdate(update);
                        System.out.println(rowsAffected > 0 ? "User updated successfully!" : "User not found.");
                        break;

                    case 4:
                        System.out.print("Enter user ID to delete: ");
                        int deleteId = scanner.nextInt();
                        String delete = "DELETE FROM users WHERE id = " + deleteId;
                        int rowsDeleted = stmt.executeUpdate(delete);
                        System.out.println(rowsDeleted > 0 ? "User deleted successfully!" : "User not found.");
                        break;

                    case 5:
                        System.out.println("Exiting program.");
                        break;

                    default:
                        System.out.println("Invalid choice. Please try again.");
                }
            } while (choice != 5);
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                if (connection != null) connection.close();
                scanner.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
