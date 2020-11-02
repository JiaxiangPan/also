/* also: Advanced Logic Synthesis and Optimization tool
 * Copyright (C) 2019- Ningbo University, Ningbo, China */

/**
 * @file stochastic.hpp
 *
 * @brief stochastic circuit synthesis
 *
 * @author Zhufei
 * @since  0.1
 */

#ifndef STOCHASTIC_HPP
#define STOCHASTIC_HPP

#include <fstream>
#include "../core/exact_sto_m3ig.hpp"

namespace alice
{

  class stochastic_command : public command
  {
    public:
      explicit stochastic_command( const environment::ptr& env ) : command( env, "stochastic circuit synthesis" )
      {
        add_option( "filename, -f", filename, "the input txt file name" );
        add_flag( "--verbose, -v", "verbose output" );
      }
    
    protected:
      void execute()
      {
        std::string line;
        std::ifstream myfile( filename );

        if( myfile.is_open() )
        {
          unsigned line_index = 0u;

          while( std::getline( myfile, line ) )
          {
            if( line_index == 0u ) { num_vars = std::stoi( line ); } 
            if( line_index == 1u ) { n = std::stoi( line ); } 
            if( line_index == 2u ) { m = std::stoi( line ); } 

            if( line_index == 3u ) 
            {
              std::stringstream ss( line );

              unsigned tmp;

              while( ss >> tmp )
              {
                vector.push_back( tmp );
              }
            }
            line_index++;
          }

          myfile.close();


          if( is_set( "verbose" ) )
          {
            std::cout << " num_vars : " << num_vars << "\n" 
                      << " n        : " << n << "\n"
                      << " m        : " << m << std::endl;

            std::cout << "Problem vector: ";
            for( auto const& e : vector )
            {
              std::cout << e << " ";
            }
            std::cout << std::endl;
          }

          stochastic_synthesis( num_vars, n, m, vector );
        }
        else
        {
          std::cerr << "Cannot open input file \n"; 
        }
      }

    private:
      std::string filename = "vector.txt";

      unsigned num_vars; //the number of variables
      unsigned n; //the highest power
      unsigned m; //the number control the accuracy 
      std::vector<unsigned> vector;
  };

  ALICE_ADD_COMMAND( stochastic, "Various" )
}

#endif