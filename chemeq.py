import numpy as np
import copy
def parse_elem(res:dict, fml:str):
    name, fac, i = "", "", 0
    if fml and fml[0].isupper():
        i = 1
        if i < len(fml) and fml[i].islower():
            i += 1
        name = fml[:i]
        while i < len(fml) and fml[i].isnumeric():
            fac += fml[i]
            i += 1
    if name:
        if not fac:
            fac = "1"
        if name in res:
            res[name] += int(fac)
        else:
            res[name] = int(fac)

    return fml[i:], i>0

def parse_term(fml:str):
    cnt, fac, term, rem = 0, "", "", ""
    if fml and fml[0] in "{[(":
        cnt += 1
        i = 1
        while i < len(fml) and cnt > 0:
            term += fml[i]
            if fml[i] in "{[(":
                cnt += 1
            if fml[i] in ")]}":
                cnt -= 1
            i += 1
        term = term[:-1]
        while i < len(fml) and fml[i].isnumeric():
            fac += fml[i]
            i += 1
        rem = fml[i:]
        if not fac:
            fac = "1"
    return term, rem, int(fac) if fac else 0
        
def res_join(pref:dict, res:dict, fac:int):
    for k,v in res.items():
        if k in pref:
            pref[k] += v*fac
        else:
            pref[k] = v*fac

def fml_clear(fml:str):
    res = ""
    for c in fml:
        if c.isalnum() or c in "(+)":
            res += c
    return res

def fml_count(fml:str):
    res, rem = {}, fml
    while rem:
        rem, els = parse_elem(res, rem)
        if not els:
            term, rem, fac = parse_term(rem)
            res_join(res,fml_count(term),fac)
    return res

class Coefficients:
    def __init__(self, coeffs, depth) -> None:
        self.coeffs = coeffs
        if depth:
            self.depth = depth
        else:
            self.depth = max(np.max(coeffs[0]), np.max(coeffs[1]))

    def __str__(self):
        return f"{[i[0] for i in self.coeffs[0]]} {[i[0] for i in self.coeffs[1]]}"
    def same(self, coeffs):
        if self.depth != coeffs.depth:
            return False
        for i in range(2):
            if not np.array_equal(self.coeffs[i], coeffs.coeffs[i]):
                return False
        return True
    
class Equation:
    def __init__(self, fl:str, fr:str):
        self.compname = (fml_clear(fl).split("+"), fml_clear(fr).split("+"))
        if not all(self.compname):
            raise ValueError("Invalid input")
        compounds = (list(map(fml_count, self.compname[0])), list(map(fml_count, self.compname[1])))
        def all_elems(side):
            elems = set()
            for cnt in side:
                elems.update(cnt.keys())
            return elems
        elem_map = all_elems(compounds[0])
        if elem_map != all_elems(compounds[1]):
            raise TypeError("Not matching elements types")
        self.elems = list(elem_map)
        self.elem_map = {self.elems[i]: i for i in range(len(self.elems))}
        self.compounds = tuple(np.array([[0 for _ in elem_map] for _ in compounds[i]]) for i in range(2))
        for i in range(2):
            for j in range(len(compounds[i])):
                for k,v in compounds[i][j].items():
                    self.compounds[i][j][self.elem_map[k]] = v

        self.cof_tree = [Coefficients(tuple(np.array([[1] for _ in self.compounds[i]]) for i in range(2)), 1)]
        print(self.elems, self.elem_map)        

    def cofinsert(self, coeffs:Coefficients):
        if not any(filter(lambda c: c.same(coeffs), self.cof_tree)):
            self.cof_tree.append(coeffs)

    def eqcheck(self, coflim=20):
        trials = []
        while len(trials) < 40000:
            cof = self.cof_tree.pop(0)
            trials.append(cof.__str__())
            eqsum = [np.sum(cof.coeffs[i] * self.compounds[i], axis=0) for i in range(2)]
            if np.array_equal(eqsum[0], eqsum[1]):
                return tuple([(cof.coeffs[i][j][0] if cof.coeffs[i][j][0] > 1 else "", self.compname[i][j]) for j in range(len(cof.coeffs[i]))] for i in range(2)), trials
            for i in range(2):
                for j in range(len(cof.coeffs[i])):
                    ncof = copy.deepcopy(cof.coeffs)
                    ncof[i][j] += 1
                    if ncof[i][j] <= coflim:
                        self.cofinsert(Coefficients(ncof,max(cof.depth, ncof[i][j])))
        print(len(trials))
        raise TimeoutError("Cannot find solution")

if __name__ == "__main__":
    # eq = Equation("K4[Fe(SCN)6] + K2Cr2O7 + H2SO4", "Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3")
    eq = Equation("  S    +   HNO3  "," H2SO4   +    NO2   +   H2O")
    print(eq.eqcheck())
    # def binsert(v:int, vs:list[int]):
    #     il, ih = 0, len(vs)

