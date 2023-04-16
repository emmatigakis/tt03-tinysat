import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

async def test_prod_term(dut, i1, i2, i3, i4, x):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.load.value = 0
    dut.run.value = 0
    dut.data.value = 0

    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut.load.value = 1

    dut._log.info("loading coefficients")
    for i in range(16):
        dut.data.value = 0
        await ClockCycles(dut.clk, 1)
    for i in range(16):
        if i == 0: 
            dut.data.value = i1
        elif i == 4:
            dut.data.value = i2
        elif i == 8:
            dut.data.value = i3
        elif i == 15:
            dut.data.value = i4
        else:
            dut.data.value = 7
        await ClockCycles(dut.clk, 1)
    for i in range(16):
        dut.data.value = 0
        await ClockCycles(dut.clk, 1)
    for i in range(16):
        dut.data.value = 0
        await ClockCycles(dut.clk, 1)

    dut._log.info("check solution")
    dut.load.value = 0
    dut.run.value = 1
    while int(dut.done.value) == 0:
        await ClockCycles(dut.clk, 1)
    assert int(dut.sol.value) == 1
    assert int(dut.x.value) == x

async def test_trivial_clause(dut, k):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.load.value = 0
    dut.run.value = 0
    dut.data.value = 0

    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut.load.value = 1

    dut._log.info("loading coefficients")
    for i in range(16):
        dut.data.value = 0
        await ClockCycles(dut.clk, 1)
    for i in range(16):
        if i == 0: 
            dut.data.value = k
        else:
            dut.data.value = 7
        await ClockCycles(dut.clk, 1)
    for i in range(16):
        if i == 0: 
            dut.data.value = -k
        else:
            dut.data.value = 0
        await ClockCycles(dut.clk, 1)
    for i in range(16):
        dut.data.value = 0
        await ClockCycles(dut.clk, 1)

    dut.load.value = 0
    dut.run.value = 1
    while int(dut.done.value) == 0:
        await ClockCycles(dut.clk, 1)
    assert int(dut.sol.value) == 1

async def test_single_2clause(dut, k1, k2):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.load.value = 0
    dut.run.value = 0
    dut.data.value = 0

    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut.load.value = 1

    dut._log.info("loading coefficients")
    for i in range(16):
        dut.data.value = 0
        await ClockCycles(dut.clk, 1)
    for i in range(16):
        if i == 0: 
            dut.data.value = k1
        else:
            dut.data.value = 7
        await ClockCycles(dut.clk, 1)
    for i in range(16):
        if i == 0: 
            dut.data.value = k2
        else:
            dut.data.value = 0
        await ClockCycles(dut.clk, 1)
    for i in range(16):
        dut.data.value = 0
        await ClockCycles(dut.clk, 1)

    dut.load.value = 0
    dut.run.value = 1
    while int(dut.done.value) == 0:
        await ClockCycles(dut.clk, 1)
    assert int(dut.sol.value) == 1
    x = int(dut.x.value)
    f1 = 1 << (k1-1)
    f2 = 1 << (k2-1)
    assert (x&f1) or (x&f2)

@cocotb.test()
async def test_tinysat1(dut):
    await test_prod_term(dut,1,2,3,4, 15)
@cocotb.test()
async def test_tinysat2(dut):
    await test_prod_term(dut,-1,-2,-3,-4, 0)
@cocotb.test()
async def test_tinysat3(dut):
    await test_prod_term(dut,-1,2,3,4, 14)
@cocotb.test()
async def test_tinysat4(dut):
    await test_prod_term(dut,1,-2,3,4, 13)
@cocotb.test()
async def test_tinysat5(dut):
    await test_prod_term(dut,1,2,-3,4, 11)
@cocotb.test()
async def test_tinysat6(dut):
    await test_prod_term(dut,1,2,3,-4, 7)
@cocotb.test()
async def test_trivial_clause1(dut):
    await test_trivial_clause(dut,1)
@cocotb.test()
async def test_trivial_clause_1(dut):
    await test_trivial_clause(dut,-1)
@cocotb.test()
async def test_trivial_clause2(dut):
    await test_trivial_clause(dut,2)
@cocotb.test()
async def test_trivial_clause_2(dut):
    await test_trivial_clause(dut,-2)
@cocotb.test()
async def test_trivial_clause3(dut):
    await test_trivial_clause(dut,3)
@cocotb.test()
async def test_trivial_clause_3(dut):
    await test_trivial_clause(dut,-3)
@cocotb.test()
async def test_trivial_clause4(dut):
    await test_trivial_clause(dut,4)
@cocotb.test()
async def test_trivial_clause_4(dut):
    await test_trivial_clause(dut,-4)
@cocotb.test()
async def test_trivial_clause5(dut):
    await test_trivial_clause(dut,5)
@cocotb.test()
async def test_trivial_clause_5(dut):
    await test_trivial_clause(dut,-5)
@cocotb.test()
async def test_trivial_clause6(dut):
    await test_trivial_clause(dut,6)
@cocotb.test()
async def test_trivial_clause_6(dut):
    await test_trivial_clause(dut,-6)
@cocotb.test()
async def test_single_2clause1(dut):
    await test_single_2clause(dut,1,2)
@cocotb.test()
async def test_single_2clause2(dut):
    await test_single_2clause(dut,2,3)
@cocotb.test()
async def test_single_2clause3(dut):
    await test_single_2clause(dut,3,4)
@cocotb.test()
async def test_single_2clause4(dut):
    await test_single_2clause(dut,4,1)
