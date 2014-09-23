using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NJLicenseNumberGenerator
{
    class Program
    {
        // Based on: http://www.highprogrammer.com/alan/numbers/dl_us_nj.html
        // Number format: Lllll fffmm MMyye
        static void Main(string[] args)
        {
            string licenseNumber = "Allll fffmm MMyye"; 
            EyeColor color = EyeColor.Brown;

            string firstName, middleName, lastName;
            

            Console.WriteLine("Enter full name (middle name optional):");
            Console.WriteLine("\tLAST, FIRST (MIDDLE)\n\tFIRST (MIDDLE) LAST");
            string fullName = Console.ReadLine();

            string[] splitName;
            if (fullName.Contains(','))
            {
                splitName = fullName.Split(new char[] { ',', ' ' });
            }
            else
            {
                splitName = fullName.Split(new char[] { ' ' });
            }
            

            licenseNumber = licenseNumber.Replace("A", "S");
            licenseNumber = licenseNumber.Replace("llll", "0000");
            licenseNumber = licenseNumber.Replace("fff", "111");
            licenseNumber = licenseNumber.Replace("mm", ConvertMiddleInitial("Joseph"));
            Console.WriteLine(String.Format("\n\"{0}\"\n", licenseNumber));

            //// TODO: Check if valid name, split into first, middle initial, last name
            //splitName = (fullName.Contains(',') ? fullName.Split(new char[] { ',', ' ' }) : fullName.Split(new char[] { ' ' }));

            Console.WriteLine("Enter birth month/year (MM/YYYY)");
            string birthday = Console.ReadLine();

            licenseNumber = licenseNumber.Replace("MM", "06");
            licenseNumber = licenseNumber.Replace("yy", "84");
            
            Console.WriteLine(String.Format("\n\"{0}\"\n", licenseNumber));

            Console.WriteLine("Choose an eye color:");
            foreach (var eyeColor in Enum.GetNames(typeof(EyeColor)))
            {
                Console.WriteLine(String.Format(" {0}) {1}", (int)Enum.Parse(typeof(EyeColor), eyeColor), eyeColor.ToString()));
            }
            string sEyeColor = Console.ReadLine();
            // TODO: Detect number or string input and assign accordingly

            licenseNumber = licenseNumber.Replace("e", ((int)color).ToString());

            Console.WriteLine(String.Format("\n\"{0}\"\n", licenseNumber));

            Console.Read();
        }

        static string ConvertMiddleInitial(string middleName)
        {
            if (string.IsNullOrEmpty(middleName) || string.IsNullOrWhiteSpace(middleName))
                return "00";
            else
            {
                char mInitial = Char.ToUpper(middleName[0]);

                // Conversion of ASCII (http://www.asciitable.com/) to driver's license encodings are offset based on the letter value:
                //      -4 for A to I, -3 for J to R, -1 for S to Z
                // Format:  {letter} ({ASCII} > {NJDL})
                if (IsCharacterBetween(mInitial, 'A', 'I')) // A (65 > 61) to I (73 > 69)
                    return ((int)mInitial - 4).ToString();
                else if (IsCharacterBetween(mInitial, 'J', 'R')) // J (74 > 71) to R (82 > 79)
                    return ((int)mInitial - 3).ToString();
                else if (IsCharacterBetween(mInitial, 'S', 'Z')) // S (83 > 82) to Z (90 > 89)
                    return ((int)mInitial - 1).ToString();
                else
                    throw new Exception(mInitial + " is not a valid middle initial");
            }
        }

        // Helper method for ConvertMiddleInitial() - determines if {low} <= {c} <= {high} by comparing ASCII character's decimal values
        static bool IsCharacterBetween(char c, char low, char high)
        {
            int cInt = (int)c;
            return cInt >= (int)low && cInt <= (int)high;
        }

        enum EyeColor
        {
             Black = 1
            ,Brown = 2
            ,Grey = 3
            ,Blue = 4
            ,Hazel = 5
            ,Green = 6
        }
    }
}
