using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AgeDisparity
{
    class Program
    {
        static void Main(string[] args)
        {
            for (int i = 12; i < 40; i++)
            {
                CalculateAge(i);      
            }

            Console.Read();
        }

        static void CalculateAge(int age)
        {
            Console.Write(String.Format("\nIf you're {0}, ", age));

            decimal minAge, maxAge;
            minAge = Math.Ceiling((decimal)age/2 + 7);
            maxAge = Math.Round((decimal)(age - 7) * 2);

            if(age <= 12 || minAge <= 12)
                Console.WriteLine("you shouldn't even be dating. Eww...");
            else if(minAge == maxAge)
                Console.WriteLine(String.Format("you can date {0} year-olds.", minAge));
            else if(minAge > maxAge)
                Console.WriteLine(String.Format("you can date {0}-{1} year-olds.", maxAge, minAge));
            else
                Console.WriteLine(String.Format("you can date {0}-{1} year-olds.", minAge, maxAge));
        }
    }
}
