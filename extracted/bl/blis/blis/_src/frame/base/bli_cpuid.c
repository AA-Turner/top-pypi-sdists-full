/*

   BLIS
   An object-based framework for developing high-performance BLAS-like
   libraries.

   Copyright (C) 2014, The University of Texas at Austin
   Copyright (C) 2018-2019, Advanced Micro Devices, Inc.
   Copyright (C) 2019, Dave Love, University of Manchester

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are
   met:
    - Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    - Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    - Neither the name(s) of the copyright holder(s) nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
   HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

*/

#if 0
  // Used only during standalone testing of ARM support.
  #include "bli_system.h"
  #include "bli_type_defs.h"
  #include "bli_cpuid.h"
  #undef __x86_64__
  #undef _M_X64
  #undef __i386
  #undef _M_IX86
  #define __arm__
#endif

#ifdef BLIS_CONFIGURETIME_CPUID
  #define BLIS_EXPORT_BLIS
  #include "bli_system.h"
  #include "bli_type_defs.h"
  #include "bli_cpuid.h"
  #include "bli_arch.h"
#else
  #include "blis.h"
#endif

// -----------------------------------------------------------------------------

#if (defined(__x86_64__) || defined(_M_X64) || defined(__i386) || defined(_M_IX86))

// This has a conflicting definition in intrin.h on Windows
#include "cpuid.h"

arch_t bli_cpuid_query_id( void )
{
	uint32_t vendor, family, model, features;

	// Call the CPUID instruction and parse its results into a family id,
	// model id, and a feature bit field. The return value encodes the
	// vendor.
	vendor = bli_cpuid_query( &family, &model, &features );

#if 0
	printf( "vendor   = %s\n", vendor==1 ? "AMD": "INTEL" );
	printf("family    = %x\n", family );
	printf( "model    = %x\n", model );
	
	printf( "features = %x\n", features );
#endif

	if ( vendor == VENDOR_INTEL )
	{
		// Check for each Intel configuration that is enabled, check for that
		// microarchitecture. We check from most recent to most dated.
#ifdef BLIS_CONFIG_SKX
		if ( bli_cpuid_is_skx( family, model, features ) )
			return BLIS_ARCH_SKX;
#endif
#ifdef BLIS_CONFIG_KNL
		if ( bli_cpuid_is_knl( family, model, features ) )
			return BLIS_ARCH_KNL;
#endif
#ifdef BLIS_CONFIG_HASWELL
		if ( bli_cpuid_is_haswell( family, model, features ) )
			return BLIS_ARCH_HASWELL;
#endif
#ifdef BLIS_CONFIG_SANDYBRIDGE
		if ( bli_cpuid_is_sandybridge( family, model, features ) )
			return BLIS_ARCH_SANDYBRIDGE;
#endif
#ifdef BLIS_CONFIG_PENRYN
		if ( bli_cpuid_is_penryn( family, model, features ) )
			return BLIS_ARCH_PENRYN;
#endif
		// If none of the other sub-configurations were detected, return
		// the 'generic' arch_t id value.
		return BLIS_ARCH_GENERIC;
	}
	else if ( vendor == VENDOR_AMD )
	{

		// Check for each AMD configuration that is enabled, check for that
		// microarchitecture. We check from most recent to most dated.
#ifdef BLIS_CONFIG_ZEN2
		if ( bli_cpuid_is_zen2( family, model, features ) )
			return BLIS_ARCH_ZEN2;
#endif
#ifdef BLIS_CONFIG_ZEN
		if ( bli_cpuid_is_zen( family, model, features ) )
			return BLIS_ARCH_ZEN;
#endif
#ifdef BLIS_CONFIG_EXCAVATOR
		if ( bli_cpuid_is_excavator( family, model, features ) )
			return BLIS_ARCH_EXCAVATOR;
#endif
#ifdef BLIS_CONFIG_STEAMROLLER
		if ( bli_cpuid_is_steamroller( family, model, features ) )
			return BLIS_ARCH_STEAMROLLER;
#endif
#ifdef BLIS_CONFIG_PILEDRIVER
		if ( bli_cpuid_is_piledriver( family, model, features ) )
			return BLIS_ARCH_PILEDRIVER;
#endif
#ifdef BLIS_CONFIG_BULLDOZER
		if ( bli_cpuid_is_bulldozer( family, model, features ) )
			return BLIS_ARCH_BULLDOZER;
#endif
		// If none of the other sub-configurations were detected, return
		// the 'generic' arch_t id value.
		return BLIS_ARCH_GENERIC;
	}
	else if ( vendor == VENDOR_UNKNOWN )
	{
		return BLIS_ARCH_GENERIC;
	}

	return BLIS_ARCH_GENERIC;
}

// -----------------------------------------------------------------------------

bool_t bli_cpuid_is_skx
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX      |
	                          FEATURE_FMA3     |
	                          FEATURE_AVX2     |
	                          FEATURE_AVX512F  |
	                          FEATURE_AVX512DQ |
	                          FEATURE_AVX512BW |
	                          FEATURE_AVX512VL ;


	int nvpu = vpu_count();

	if ( bli_cpuid_has_features( features, expected ) )
	{
		switch ( nvpu )
		{
		case 1:
			bli_arch_log( "Hardware has 1 FMA unit; using 'haswell' (not 'skx') sub-config.\n" );
			return FALSE;
		case 2:
			bli_arch_log( "Hardware has 2 FMA units; using 'skx' sub-config.\n" );
			return TRUE;
		default:
			bli_arch_log( "Number of FMA units unknown; using 'haswell' (not 'skx') config.\n" );
			return FALSE;
		}
	}
	else
		return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_knl
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX     |
	                          FEATURE_FMA3    |
	                          FEATURE_AVX2    |
	                          FEATURE_AVX512F |
	                          FEATURE_AVX512PF;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_haswell
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX  |
	                          FEATURE_FMA3 |
	                          FEATURE_AVX2;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_sandybridge
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_penryn
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_SSE3 |
	                          FEATURE_SSSE3;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	return TRUE;
}

// -----------------------------------------------------------------------------

bool_t bli_cpuid_is_zen2
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX  |
	                          FEATURE_FMA3 |
	                          FEATURE_AVX2;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	// All Zen2 cores have a family of 0x17.
	if ( family != 0x17 ) return FALSE;

	// Finally, check for specific models:
	// - 0x30-0xff (THIS NEEDS UPDATING)
	const bool_t is_arch
	=
	( 0x30 <= model && model <= 0xff );

	if ( !is_arch ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_zen
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX  |
	                          FEATURE_FMA3 |
	                          FEATURE_AVX2;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	// All Zen cores have a family of 0x17.
	if ( family != 0x17 ) return FALSE;

	// Finally, check for specific models:
	// - 0x00-0xff (THIS NEEDS UPDATING)
	const bool_t is_arch
	=
	( 0x00 <= model && model <= 0xff );

	if ( !is_arch ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_excavator
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX  |
	                          FEATURE_FMA3 |
	                          FEATURE_AVX2;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	// All Excavator cores have a family of 0x15.
	if ( family != 0x15 ) return FALSE;

	// Finally, check for specific models:
	// - 0x60-0x7f
	const bool_t is_arch
	=
	( 0x60 <= model && model <= 0x7f );

	if ( !is_arch ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_steamroller
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX  |
	                          FEATURE_FMA3 |
	                          FEATURE_FMA4;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	// All Steamroller cores have a family of 0x15.
	if ( family != 0x15 ) return FALSE;

	// Finally, check for specific models:
	// - 0x30-0x3f
	const bool_t is_arch
	=
	( 0x30 <= model && model <= 0x3f );

	if ( !is_arch ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_piledriver
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX  |
	                          FEATURE_FMA3 |
	                          FEATURE_FMA4;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	// All Piledriver cores have a family of 0x15.
	if ( family != 0x15 ) return FALSE;

	// Finally, check for specific models:
	// - 0x02
	// - 0x10-0x1f
	const bool_t is_arch
	=
	model == 0x02 || ( 0x10 <= model && model <= 0x1f );

	if ( !is_arch ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_bulldozer
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_AVX |
	                          FEATURE_FMA4;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	// All Bulldozer cores have a family of 0x15.
	if ( family != 0x15 ) return FALSE;

	// Finally, check for specific models:
	// - 0x00
	// - 0x01
	const bool_t is_arch
	=
	( model == 0x00 || model == 0x01 );

	if ( !is_arch ) return FALSE;

	return TRUE;
}

#elif defined(__aarch64__) || defined(__arm__) || defined(_M_ARM)

arch_t bli_cpuid_query_id( void )
{
	uint32_t vendor, model, part, features;

	// Call the CPUID instruction and parse its results into a model id,
	// part id, and a feature bit field. The return value encodes the
	// vendor.
	vendor = bli_cpuid_query( &model, &part, &features );

#if 0
	printf( "vendor   = %u\n", vendor );
	printf( "model    = %u\n", model );
	printf( "part     = 0x%x\n", part );
	printf( "features = %u\n", features );
#endif



	if ( vendor == VENDOR_ARM )
	{
		if ( model == MODEL_ARMV8 )
		{
			// Check for each ARMv8 configuration that is enabled, check for that
			// microarchitecture. We check from most recent to most dated.
#ifdef BLIS_CONFIG_THUNDERX2
			if ( bli_cpuid_is_thunderx2( model, part, features ) )
				return BLIS_ARCH_THUNDERX2;
#endif
#ifdef BLIS_CONFIG_CORTEXA57
			if ( bli_cpuid_is_cortexa57( model, part, features ) )
				return BLIS_ARCH_CORTEXA57;
#endif
			// If none of the other sub-configurations were detected, return
			// the 'generic' arch_t id value.
			return BLIS_ARCH_GENERIC;
		}
		else if ( model == MODEL_ARMV7 )
		{
			// Check for each ARMv7 configuration that is enabled, check for that
			// microarchitecture. We check from most recent to most dated.
#ifdef BLIS_CONFIG_CORTEXA15
			if ( bli_cpuid_is_cortexa15( model, part, features ) )
				return BLIS_ARCH_CORTEXA15;
#endif
#ifdef BLIS_CONFIG_CORTEXA9
			if ( bli_cpuid_is_cortexa9( model, part, features ) )
				return BLIS_ARCH_CORTEXA9;
#endif
			// If none of the other sub-configurations were detected, return
			// the 'generic' arch_t id value.
			return BLIS_ARCH_GENERIC;
		}
	}
	else if ( vendor == VENDOR_UNKNOWN )
	{
		return BLIS_ARCH_GENERIC;
	}

	return BLIS_ARCH_GENERIC;
}

bool_t bli_cpuid_is_thunderx2
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_NEON;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_cortexa57
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_NEON;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_cortexa53
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_NEON;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_cortexa15
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_NEON;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	return TRUE;
}

bool_t bli_cpuid_is_cortexa9
     (
       uint32_t family,
       uint32_t model,
       uint32_t features
     )
{
	// Check for expected CPU features.
	const uint32_t expected = FEATURE_NEON;

	if ( !bli_cpuid_has_features( features, expected ) ) return FALSE;

	return TRUE;
}

#endif

// -----------------------------------------------------------------------------

//
// This section of the file was based off of cpuid.cxx from TBLIS [1].
//
// [1] https://github.com/devinamatthews/tblis
//

/*

   Copyright (C) 2017, The University of Texas at Austin
   Copyright (C) 2017, Devin Matthews
   Copyright (C) 2018 - 2019, Advanced Micro Devices, Inc.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are
   met:
    - Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    - Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    - Neither the name(s) of the copyright holder(s) nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
   HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

*/

#if defined(__x86_64__) || defined(_M_X64) || defined(__i386) || defined(_M_IX86)

enum
{
                                      // input register(s)     output register
	FEATURE_MASK_SSE3     = (1u<< 0), // cpuid[eax=1]         :ecx[0]
	FEATURE_MASK_SSSE3    = (1u<< 9), // cpuid[eax=1]         :ecx[9]
	FEATURE_MASK_SSE41    = (1u<<19), // cpuid[eax=1]         :ecx[19]
	FEATURE_MASK_SSE42    = (1u<<20), // cpuid[eax=1]         :ecx[20]
	FEATURE_MASK_AVX      = (1u<<28), // cpuid[eax=1]         :ecx[28]
	FEATURE_MASK_AVX2     = (1u<< 5), // cpuid[eax=7,ecx=0]   :ebx[5]
	FEATURE_MASK_FMA3     = (1u<<12), // cpuid[eax=1]         :ecx[12]
	FEATURE_MASK_FMA4     = (1u<<16), // cpuid[eax=0x80000001]:ecx[16]
	FEATURE_MASK_AVX512F  = (1u<<16), // cpuid[eax=7,ecx=0]   :ebx[16]
	FEATURE_MASK_AVX512DQ = (1u<<17), // cpuid[eax=7,ecx=0]   :ebx[17]
	FEATURE_MASK_AVX512PF = (1u<<26), // cpuid[eax=7,ecx=0]   :ebx[26]
	FEATURE_MASK_AVX512ER = (1u<<27), // cpuid[eax=7,ecx=0]   :ebx[27]
	FEATURE_MASK_AVX512CD = (1u<<28), // cpuid[eax=7,ecx=0]   :ebx[28]
	FEATURE_MASK_AVX512BW = (1u<<30), // cpuid[eax=7,ecx=0]   :ebx[30]
	FEATURE_MASK_AVX512VL = (1u<<31), // cpuid[eax=7,ecx=0]   :ebx[31]
	FEATURE_MASK_XGETBV   = (1u<<26)|
                            (1u<<27), // cpuid[eax=1]         :ecx[27:26]
	XGETBV_MASK_XMM       = 0x02u,    // xcr0[1]
	XGETBV_MASK_YMM       = 0x04u,    // xcr0[2]
	XGETBV_MASK_ZMM       = 0xe0u     // xcr0[7:5]
};


uint32_t bli_cpuid_query
     (
       uint32_t* family,
       uint32_t* model,
       uint32_t* features
     )
{
	uint32_t eax, ebx, ecx, edx;

	uint32_t old_model  = 0;
	uint32_t old_family = 0;
	uint32_t ext_model  = 0;
	uint32_t ext_family = 0;

	*family   = 0;
	*model    = 0;
	*features = 0;

	//fprintf( stderr, "checking cpuid\n" );

	uint32_t cpuid_max     = __get_cpuid_max( 0,           0 );
	uint32_t cpuid_max_ext = __get_cpuid_max( 0x80000000u, 0 );

	//fprintf( stderr, "max cpuid leaf: %d\n", cpuid_max );
	//fprintf( stderr, "max extended cpuid leaf: %08x\n", cpuid_max_ext );

	if ( cpuid_max < 1 ) return VENDOR_UNKNOWN;

	// The fourth '0' serves as the NULL-terminator for the vendor string.
	uint32_t vendor_string[4] = { 0, 0, 0, 0 };

	// This is actually a macro that modifies the last four operands,
	// hence why they are not passed by address.
	__cpuid( 0, eax, vendor_string[0],
	                 vendor_string[2],
	                 vendor_string[1] );

	// Check extended feature bits for post-AVX2 features.
	if ( cpuid_max >= 7 )
	{
		// This is actually a macro that modifies the last four operands,
		// hence why they are not passed by address.
		__cpuid_count( 7, 0, eax, ebx, ecx, edx );

		//fprintf( stderr, "cpuid leaf 7:\n" );
		//print_binary( eax );
		//print_binary( ebx );
		//print_binary( ecx );
		//print_binary( edx );

		if ( bli_cpuid_has_features( ebx, FEATURE_MASK_AVX2     ) ) *features |= FEATURE_AVX2;
		if ( bli_cpuid_has_features( ebx, FEATURE_MASK_AVX512F  ) ) *features |= FEATURE_AVX512F;
		if ( bli_cpuid_has_features( ebx, FEATURE_MASK_AVX512DQ ) ) *features |= FEATURE_AVX512DQ;
		if ( bli_cpuid_has_features( ebx, FEATURE_MASK_AVX512PF ) ) *features |= FEATURE_AVX512PF;
		if ( bli_cpuid_has_features( ebx, FEATURE_MASK_AVX512ER ) ) *features |= FEATURE_AVX512ER;
		if ( bli_cpuid_has_features( ebx, FEATURE_MASK_AVX512CD ) ) *features |= FEATURE_AVX512CD;
		if ( bli_cpuid_has_features( ebx, FEATURE_MASK_AVX512BW ) ) *features |= FEATURE_AVX512BW;
		if ( bli_cpuid_has_features( ebx, FEATURE_MASK_AVX512VL ) ) *features |= FEATURE_AVX512VL;
	}

	// Check extended processor info / features bits for AMD-specific features.
	if ( cpuid_max_ext >= 0x80000001u )
	{
		// This is actually a macro that modifies the last four operands,
		// hence why they are not passed by address.
		__cpuid( 0x80000001u, eax, ebx, ecx, edx );

		//fprintf(stderr, "extended cpuid leaf 0x80000001:\n");
		//print_binary(eax);
		//print_binary(ebx);
		//print_binary(ecx);
		//print_binary(edx);

		if ( bli_cpuid_has_features( ecx, FEATURE_MASK_FMA4 ) ) *features |= FEATURE_FMA4;
	}

	// Unconditionally check processor info / features bits.
	{
		// This is actually a macro that modifies the last four operands,
		// hence why they are not passed by address.
		__cpuid( 1, eax, ebx, ecx, edx );

		//fprintf(stderr, "cpuid leaf 1:\n");
		//print_binary(eax);
		//print_binary(ebx);
		//print_binary(ecx);
		//print_binary(edx);

		/*
		   cpuid(eax=1): eax[27:0]

			3: 0 - Stepping
			7: 4 - Model
		   11: 8 - Family
		   13:12 - Processor Type
		   19:16 - Extended Model
		   27:20 - Extended Family

		   Intel and AMD have suggested applications to display the family of a
		   CPU as the sum of the "Family" and the "Extended Family" fields shown
		   above, and the model as the sum of the "Model" and the 4-bit
		   left-shifted "Extended Model" fields. If "Family" is different than
		   6 or 15, only the "Family" and "Model" fields should be used while the
		   "Extended Family" and "Extended Model" bits are reserved. If "Family"
		   is set to 15, then "Extended Family" and the 4-bit left-shifted
		   "Extended Model" should be added to the respective base values, and if
		   "Family" is set to 6, then only the 4-bit left-shifted "Extended Model"
		   should be added to "Model".
		*/

		old_model  = ( eax >>  4 ) & ( 0xF  ); // bits 7:4
		old_family = ( eax >>  8 ) & ( 0xF  ); // bits 11:8

		ext_model  = ( eax >> 16 ) & ( 0xF  ); // bits 19:16
		ext_family = ( eax >> 20 ) & ( 0xFF ); // bits 27:20

		// Set the display model and family values based on the original family
		// value. See explanation above.
		if      ( old_family == 6 )
		{
			*model  = ( ext_model << 4 ) + old_model;
			*family =                      old_family;
		}
		else if ( old_family == 15 )
		{
			*model  = ( ext_model << 4 ) + old_model;
			*family = ( ext_family     ) + old_family;
		}
		else
		{
			*model  =                      old_model;
			*family =                      old_family;
		}

		// Check for SSE, AVX, and FMA3 features.
		if ( bli_cpuid_has_features( ecx, FEATURE_MASK_SSE3  ) ) *features |= FEATURE_SSE3;
		if ( bli_cpuid_has_features( ecx, FEATURE_MASK_SSSE3 ) ) *features |= FEATURE_SSSE3;
		if ( bli_cpuid_has_features( ecx, FEATURE_MASK_SSE41 ) ) *features |= FEATURE_SSE41;
		if ( bli_cpuid_has_features( ecx, FEATURE_MASK_SSE42 ) ) *features |= FEATURE_SSE42;
		if ( bli_cpuid_has_features( ecx, FEATURE_MASK_AVX   ) ) *features |= FEATURE_AVX;
		if ( bli_cpuid_has_features( ecx, FEATURE_MASK_FMA3  ) ) *features |= FEATURE_FMA3;

		// Check whether the hardware supports xsave/xrestor/xsetbv/xgetbv AND 
		// support for these is enabled by the OS. If so, then we proceed with
		// checking that various register-state saving features are available.
		if ( bli_cpuid_has_features( ecx, FEATURE_MASK_XGETBV ) )
		{
			uint32_t xcr = 0;

			// Call xgetbv to get xcr0 (the extended control register) copied
			// to [edx:eax]. This encodes whether software supports various
			// register state-saving features.
			__asm__ __volatile__
			(
				".byte 0x0F, 0x01, 0xD0"
				: "=a" (eax),
				  "=d" (edx)
				: "c"  (xcr)
				: "cc"
			);

			//fprintf(stderr, "xcr0:\n");
			//print_binary(eax);
			//print_binary(edx);

			//fprintf(stderr, "xgetbv: xmm: %d\n", bli_cpuid_has_features(eax, XGETBV_MASK_XMM));
			//fprintf(stderr, "xgetbv: ymm: %d\n", bli_cpuid_has_features(eax, XGETBV_MASK_XMM|
			//                                                XGETBV_MASK_YMM));
			//fprintf(stderr, "xgetbv: zmm: %d\n", bli_cpuid_has_features(eax, XGETBV_MASK_XMM|
			//                                                XGETBV_MASK_YMM|
			//                                                XGETBV_MASK_ZMM));

			// The OS can manage the state of 512-bit zmm (AVX-512) registers
			// only if the xcr[7:5] bits are set. If they are not set, then
			// clear all feature bits related to AVX-512. 
			if ( !bli_cpuid_has_features( eax, XGETBV_MASK_XMM |
				                               XGETBV_MASK_YMM |
				                               XGETBV_MASK_ZMM ) )
			{
				*features &= ~( FEATURE_AVX512F  |
				                FEATURE_AVX512DQ |
				                FEATURE_AVX512PF |
				                FEATURE_AVX512ER |
				                FEATURE_AVX512CD |
				                FEATURE_AVX512BW |
				                FEATURE_AVX512VL );
			}

			// The OS can manage the state of 256-bit ymm (AVX) registers
			// only if the xcr[2] bit is set. If it is not set, then
			// clear all feature bits related to AVX. 
			if ( !bli_cpuid_has_features( eax, XGETBV_MASK_XMM |
				                               XGETBV_MASK_YMM ) )
			{
				*features &= ~( FEATURE_AVX  |
				                FEATURE_AVX2 |
				                FEATURE_FMA3 |
				                FEATURE_FMA4 );
			}

			// The OS can manage the state of 128-bit xmm (SSE) registers
			// only if the xcr[1] bit is set. If it is not set, then
			// clear all feature bits related to SSE (which means the
			// entire bitfield is clear). 
			if ( !bli_cpuid_has_features( eax, XGETBV_MASK_XMM ) )
			{
				*features = 0;
			}
		}
		else
		{
			// If the hardware does not support xsave/xrestor/xsetbv/xgetbv,
			// OR these features are not enabled by the OS, then we clear
			// the bitfield, because it means that not even xmm support is
			// present.

			//fprintf(stderr, "xgetbv: no\n");
			features = 0;
		}
	}

	//fprintf(stderr, "vendor: %12s\n", vendor_string);
	//fprintf(stderr, "family: %d\n", family);
	//fprintf(stderr, "model: %d\n", model);
	//fprintf(stderr, "sse3: %d\n", bli_cpuid_has_features(features, FEATURE_SSE3));
	//fprintf(stderr, "ssse3: %d\n", bli_cpuid_has_features(features, FEATURE_SSSE3));
	//fprintf(stderr, "sse4.1: %d\n", bli_cpuid_has_features(features, FEATURE_SSE41));
	//fprintf(stderr, "sse4.2: %d\n", bli_cpuid_has_features(features, FEATURE_SSE42));
	//fprintf(stderr, "avx: %d\n", bli_cpuid_has_features(features, FEATURE_AVX));
	//fprintf(stderr, "avx2: %d\n", bli_cpuid_has_features(features, FEATURE_AVX2));
	//fprintf(stderr, "fma3: %d\n", bli_cpuid_has_features(features, FEATURE_FMA3));
	//fprintf(stderr, "fma4: %d\n", bli_cpuid_has_features(features, FEATURE_FMA4));
	//fprintf(stderr, "avx512f: %d\n", bli_cpuid_has_features(features, FEATURE_AVX512F));
	//fprintf(stderr, "avx512pf: %d\n", bli_cpuid_has_features(features, FEATURE_AVX512PF));
	//fprintf(stderr, "avx512dq: %d\n", bli_cpuid_has_features(features, FEATURE_AVX512DQ));

	// Check the vendor string and return a value to indicate Intel or AMD.
	if      ( strcmp( ( char* )vendor_string, "AuthenticAMD" ) == 0 )
		return VENDOR_AMD;
	else if ( strcmp( ( char* )vendor_string, "GenuineIntel" ) == 0 )
		return VENDOR_INTEL;
	else
		return VENDOR_UNKNOWN;
}

void get_cpu_name( char *cpu_name )
{
	uint32_t eax, ebx, ecx, edx;

	__cpuid( 0x80000002u, eax, ebx, ecx, edx );
	//printf("%x %x %x %x\n", eax, ebx, ecx, edx);

	*( uint32_t* )&cpu_name[0 + 0] = eax;
	*( uint32_t* )&cpu_name[0 + 4] = ebx;
	*( uint32_t* )&cpu_name[0 + 8] = ecx;
	*( uint32_t* )&cpu_name[0 +12] = edx;

	__cpuid( 0x80000003u, eax, ebx, ecx, edx );
	//printf("%x %x %x %x\n", eax, ebx, ecx, edx);

	*( uint32_t* )&cpu_name[16+ 0] = eax;
	*( uint32_t* )&cpu_name[16+ 4] = ebx;
	*( uint32_t* )&cpu_name[16+ 8] = ecx;
	*( uint32_t* )&cpu_name[16+12] = edx;

	__cpuid( 0x80000004u, eax, ebx, ecx, edx );
	//printf("%x %x %x %x\n", eax, ebx, ecx, edx);

	*( uint32_t* )&cpu_name[32+ 0] = eax;
	*( uint32_t* )&cpu_name[32+ 4] = ebx;
	*( uint32_t* )&cpu_name[32+ 8] = ecx;
	*( uint32_t* )&cpu_name[32+12] = edx;
}

// Return the number of FMA units _assuming avx512 is supported_.
// This needs updating for new processor types, sigh.
// See https://ark.intel.com/content/www/us/en/ark.html#@Processors
// and also https://github.com/jeffhammond/vpu-count
int vpu_count( void )
{
	char  cpu_name[48] = {};
	char* loc;
	char  model_num[5];
	int   sku;

	get_cpu_name( cpu_name );

	if ( strstr( cpu_name, "Intel(R) Xeon(R)" ) != NULL )
	{
		if (( loc = strstr( cpu_name, "Platinum" ) ))
			return 2;
		if ( loc == NULL )
			loc = strstr( cpu_name, "Gold" ); // 1 or 2, tested below
		if ( loc == NULL )
			if (( loc = strstr( cpu_name, "Silver" ) ))
				return 1;
		if ( loc == NULL )
			if (( loc = strstr( cpu_name, "Bronze" ) ))
				return 1;
		if ( loc == NULL )
			loc = strstr( cpu_name, "W" );
		if ( loc == NULL )
			if (( loc = strstr( cpu_name, "D" ) ))
				// Fixme:  May be wrong
				// <https://github.com/jeffhammond/vpu-count/issues/3#issuecomment-542044651>
				return 1;
		if ( loc == NULL )
			return -1;

		// We may have W-nnnn rather than, say, Gold nnnn
		if ( 'W' == *loc && '-' == *(loc+1) )
			loc++;
		else
			loc = strstr( loc+1, " " );
		if ( loc == NULL )
			return -1;

		strncpy( model_num, loc+1, 4 );
		model_num[4] = '\0'; // Things like i9-10900X matched above

		sku = atoi( model_num );

		// These were derived from ARK listings as of 2019-10-09, but
		// may not be complete, especially as the ARK Skylake listing
		// seems to be limited.
		if      ( 8199 >= sku && sku >= 8100 ) return 2;
		else if ( 6199 >= sku && sku >= 6100 ) return 2;
		else if (                sku == 5122 ) return 2;
		else if ( 6299 >= sku && sku >= 6200 ) return 2; // Cascade Lake Gold
		else if ( 5299 >= sku && sku >= 5200 ) return 1; // Cascade Lake Gold
		else if ( 5199 >= sku && sku >= 5100 ) return 1;
		else if ( 4199 >= sku && sku >= 4100 ) return 1;
		else if ( 3199 >= sku && sku >= 3100 ) return 1;
		else if ( 3299 >= sku && sku >= 3200 ) return 2; // Cascade Lake W
		else if ( 2299 >= sku && sku >= 2200 ) return 2; // Cascade Lake W
		else if ( 2199 >= sku && sku >= 2120 ) return 2;
		else if ( 2102 == sku || sku == 2104 ) return 2; // Gold exceptions
		else if ( 2119 >= sku && sku >= 2100 ) return 1;
		else return -1;
	}
	else if ( strstr( cpu_name, "Intel(R) Core(TM)" ) != NULL )
		return 2; // All i7/i9 with avx512?
	else
	{
		return -1;
	}
}

#elif defined(__aarch64__) || defined(__arm__) || defined(_M_ARM)

#define TEMP_BUFFER_SIZE 200

uint32_t bli_cpuid_query
     (
       uint32_t* model,
       uint32_t* part,
       uint32_t* features
     )
{
	*model    = MODEL_UNKNOWN;
    *part     = 0;
	*features = 0;

	char* pci_str = "/proc/cpuinfo";

	char  proc_str[ TEMP_BUFFER_SIZE ];
	char  ptno_str[ TEMP_BUFFER_SIZE ];
	char  feat_str[ TEMP_BUFFER_SIZE ];
	char* r_val;

	//printf( "bli_cpuid_query(): beginning search\n" );

	// Search /proc/cpuinfo for the 'Processor' entry.
	r_val = find_string_in( "Processor", proc_str, TEMP_BUFFER_SIZE, pci_str );
	if ( r_val == NULL ) return VENDOR_ARM;

	// Search /proc/cpuinfo for the 'CPU part' entry.
	r_val = find_string_in( "CPU part",  ptno_str, TEMP_BUFFER_SIZE, pci_str );
	if ( r_val == NULL ) return VENDOR_ARM;

	// Search /proc/cpuinfo for the 'Features' entry.
	r_val = find_string_in( "Features",  feat_str, TEMP_BUFFER_SIZE, pci_str );
	if ( r_val == NULL ) return VENDOR_ARM;

#if 0
	printf( "bli_cpuid_query(): full processor string: %s\n", proc_str );
	printf( "bli_cpuid_query(): full part num  string: %s\n", ptno_str );
	printf( "bli_cpuid_query(): full features  string: %s\n", feat_str );
#endif

	// Parse the feature string to check for SIMD features.
	if ( strstr( feat_str, "neon"  ) != NULL ||
	     strstr( feat_str, "asimd" ) != NULL )
		*features |= FEATURE_NEON;

	//printf( "bli_cpuid_query(): features var: %u\n", *features );

	// Parse the processor string to uncover the model.
	if      ( strstr( proc_str, "ARMv7"   ) != NULL )
		*model = MODEL_ARMV7;
	else if ( strstr( proc_str, "AArch64" ) != NULL ||
              strstr( proc_str, "ARMv8"   ) )
		*model = MODEL_ARMV8;

	//printf( "bli_cpuid_query(): model: %u\n", *model );

	// Parse the part number string.
	r_val = strstr( ptno_str, "0x" );
    if ( r_val != NULL)
    {
	    *part = strtol( r_val, NULL, 16 );
    }
	//printf( "bli_cpuid_query(): part#: %x\n", *part );

	return VENDOR_ARM;
}

char* find_string_in( char* target, char* buffer, size_t buf_len, char* filepath )
{
	// This function searches for the first line of the file located at
	// 'filepath' that contains the string 'target' and then copies that
	// line (actually, the substring of the line starting with 'target')
	// to 'buffer', which is 'buf_len' bytes long.

	char* r_val = NULL;

	// Allocate a temporary local buffer equal to the size of buffer.
	char* buf_local = malloc( buf_len * sizeof( char ) );

	// Open the file stream.
	FILE* stream = fopen( filepath, "r" );

	// Repeatedly read in a line from the stream, storing the contents of
	// the stream into buf_local.
	while ( !feof( stream ) )
	{
		// Read in the current line, up to buf_len-1 bytes.
		r_val = fgets( buf_local, buf_len-1, stream );

		//printf( "read line: %s", buf_local );

		// fgets() returns the pointer specified by the first argument (in
		// this case, buf_local) on success and NULL on error.
		if ( r_val == NULL ) break;

		// Since fgets() was successful, we can search for the target string
		// within the current line, as captured in buf_local.
		r_val = strstr( buf_local, target );

		// If the target string was found in buf_local, we save it to buffer.
		if ( r_val != NULL )
		{
			//printf( "  found match to '%s'\n", target );

			// Copy the string read by fgets() to the caller's buffer.
			strncpy( buffer, buf_local, buf_len );

			// Make sure that we have a terminating null character by the
			// end of the buffer.
			if ( buf_len > 0 ) buffer[ buf_len - 1 ] = '\0';

			// Leave the loop since we found the target string.
			break;
		}
	}

	// Close the file stream.
	fclose( stream );

	// Free the temporary local buffer.
	free( buf_local );

	// Return r_val so the caller knows if we failed.
	return r_val;
}

#endif

#ifdef __cpuid
  #undef __cpuid
#endif
