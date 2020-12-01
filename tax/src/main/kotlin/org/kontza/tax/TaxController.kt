package org.kontza.tax

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class TaxController {
    @GetMapping("/")
    fun tax(): TaxDto {
        return TaxDto("Tax", "1.0")
    }
}