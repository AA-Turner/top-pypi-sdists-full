// Copyright 2022 DeepMind Technologies Limited
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef MUJOCO_PYTHON_CODEGEN_ENUM_TRAITS_H_
#define MUJOCO_PYTHON_CODEGEN_ENUM_TRAITS_H_

#include <array>
#include <tuple>
#include <utility>

#include <mujoco/mujoco.h>

namespace mujoco::python_traits {

struct mjtDisableBit {
  static constexpr char name[] = "mjtDisableBit";
  using type = ::mjtDisableBit;
  static constexpr auto values = std::array{
    std::make_pair("mjDSBL_CONSTRAINT", ::mjtDisableBit::mjDSBL_CONSTRAINT),
    std::make_pair("mjDSBL_EQUALITY", ::mjtDisableBit::mjDSBL_EQUALITY),
    std::make_pair("mjDSBL_FRICTIONLOSS", ::mjtDisableBit::mjDSBL_FRICTIONLOSS),
    std::make_pair("mjDSBL_LIMIT", ::mjtDisableBit::mjDSBL_LIMIT),
    std::make_pair("mjDSBL_CONTACT", ::mjtDisableBit::mjDSBL_CONTACT),
    std::make_pair("mjDSBL_PASSIVE", ::mjtDisableBit::mjDSBL_PASSIVE),
    std::make_pair("mjDSBL_GRAVITY", ::mjtDisableBit::mjDSBL_GRAVITY),
    std::make_pair("mjDSBL_CLAMPCTRL", ::mjtDisableBit::mjDSBL_CLAMPCTRL),
    std::make_pair("mjDSBL_WARMSTART", ::mjtDisableBit::mjDSBL_WARMSTART),
    std::make_pair("mjDSBL_FILTERPARENT", ::mjtDisableBit::mjDSBL_FILTERPARENT),
    std::make_pair("mjDSBL_ACTUATION", ::mjtDisableBit::mjDSBL_ACTUATION),
    std::make_pair("mjDSBL_REFSAFE", ::mjtDisableBit::mjDSBL_REFSAFE),
    std::make_pair("mjDSBL_SENSOR", ::mjtDisableBit::mjDSBL_SENSOR),
    std::make_pair("mjDSBL_MIDPHASE", ::mjtDisableBit::mjDSBL_MIDPHASE),
    std::make_pair("mjDSBL_EULERDAMP", ::mjtDisableBit::mjDSBL_EULERDAMP),
    std::make_pair("mjDSBL_AUTORESET", ::mjtDisableBit::mjDSBL_AUTORESET),
    std::make_pair("mjDSBL_NATIVECCD", ::mjtDisableBit::mjDSBL_NATIVECCD),
    std::make_pair("mjNDISABLE", ::mjtDisableBit::mjNDISABLE)};
};

struct mjtEnableBit {
  static constexpr char name[] = "mjtEnableBit";
  using type = ::mjtEnableBit;
  static constexpr auto values = std::array{
    std::make_pair("mjENBL_OVERRIDE", ::mjtEnableBit::mjENBL_OVERRIDE),
    std::make_pair("mjENBL_ENERGY", ::mjtEnableBit::mjENBL_ENERGY),
    std::make_pair("mjENBL_FWDINV", ::mjtEnableBit::mjENBL_FWDINV),
    std::make_pair("mjENBL_INVDISCRETE", ::mjtEnableBit::mjENBL_INVDISCRETE),
    std::make_pair("mjENBL_MULTICCD", ::mjtEnableBit::mjENBL_MULTICCD),
    std::make_pair("mjENBL_ISLAND", ::mjtEnableBit::mjENBL_ISLAND),
    std::make_pair("mjNENABLE", ::mjtEnableBit::mjNENABLE)};
};

struct mjtJoint {
  static constexpr char name[] = "mjtJoint";
  using type = ::mjtJoint;
  static constexpr auto values = std::array{
    std::make_pair("mjJNT_FREE", ::mjtJoint::mjJNT_FREE),
    std::make_pair("mjJNT_BALL", ::mjtJoint::mjJNT_BALL),
    std::make_pair("mjJNT_SLIDE", ::mjtJoint::mjJNT_SLIDE),
    std::make_pair("mjJNT_HINGE", ::mjtJoint::mjJNT_HINGE)};
};

struct mjtGeom {
  static constexpr char name[] = "mjtGeom";
  using type = ::mjtGeom;
  static constexpr auto values = std::array{
    std::make_pair("mjGEOM_PLANE", ::mjtGeom::mjGEOM_PLANE),
    std::make_pair("mjGEOM_HFIELD", ::mjtGeom::mjGEOM_HFIELD),
    std::make_pair("mjGEOM_SPHERE", ::mjtGeom::mjGEOM_SPHERE),
    std::make_pair("mjGEOM_CAPSULE", ::mjtGeom::mjGEOM_CAPSULE),
    std::make_pair("mjGEOM_ELLIPSOID", ::mjtGeom::mjGEOM_ELLIPSOID),
    std::make_pair("mjGEOM_CYLINDER", ::mjtGeom::mjGEOM_CYLINDER),
    std::make_pair("mjGEOM_BOX", ::mjtGeom::mjGEOM_BOX),
    std::make_pair("mjGEOM_MESH", ::mjtGeom::mjGEOM_MESH),
    std::make_pair("mjGEOM_SDF", ::mjtGeom::mjGEOM_SDF),
    std::make_pair("mjNGEOMTYPES", ::mjtGeom::mjNGEOMTYPES),
    std::make_pair("mjGEOM_ARROW", ::mjtGeom::mjGEOM_ARROW),
    std::make_pair("mjGEOM_ARROW1", ::mjtGeom::mjGEOM_ARROW1),
    std::make_pair("mjGEOM_ARROW2", ::mjtGeom::mjGEOM_ARROW2),
    std::make_pair("mjGEOM_LINE", ::mjtGeom::mjGEOM_LINE),
    std::make_pair("mjGEOM_LINEBOX", ::mjtGeom::mjGEOM_LINEBOX),
    std::make_pair("mjGEOM_FLEX", ::mjtGeom::mjGEOM_FLEX),
    std::make_pair("mjGEOM_SKIN", ::mjtGeom::mjGEOM_SKIN),
    std::make_pair("mjGEOM_LABEL", ::mjtGeom::mjGEOM_LABEL),
    std::make_pair("mjGEOM_TRIANGLE", ::mjtGeom::mjGEOM_TRIANGLE),
    std::make_pair("mjGEOM_NONE", ::mjtGeom::mjGEOM_NONE)};
};

struct mjtCamLight {
  static constexpr char name[] = "mjtCamLight";
  using type = ::mjtCamLight;
  static constexpr auto values = std::array{
    std::make_pair("mjCAMLIGHT_FIXED", ::mjtCamLight::mjCAMLIGHT_FIXED),
    std::make_pair("mjCAMLIGHT_TRACK", ::mjtCamLight::mjCAMLIGHT_TRACK),
    std::make_pair("mjCAMLIGHT_TRACKCOM", ::mjtCamLight::mjCAMLIGHT_TRACKCOM),
    std::make_pair("mjCAMLIGHT_TARGETBODY", ::mjtCamLight::mjCAMLIGHT_TARGETBODY),
    std::make_pair("mjCAMLIGHT_TARGETBODYCOM", ::mjtCamLight::mjCAMLIGHT_TARGETBODYCOM)};
};

struct mjtTexture {
  static constexpr char name[] = "mjtTexture";
  using type = ::mjtTexture;
  static constexpr auto values = std::array{
    std::make_pair("mjTEXTURE_2D", ::mjtTexture::mjTEXTURE_2D),
    std::make_pair("mjTEXTURE_CUBE", ::mjtTexture::mjTEXTURE_CUBE),
    std::make_pair("mjTEXTURE_SKYBOX", ::mjtTexture::mjTEXTURE_SKYBOX)};
};

struct mjtTextureRole {
  static constexpr char name[] = "mjtTextureRole";
  using type = ::mjtTextureRole;
  static constexpr auto values = std::array{
    std::make_pair("mjTEXROLE_USER", ::mjtTextureRole::mjTEXROLE_USER),
    std::make_pair("mjTEXROLE_RGB", ::mjtTextureRole::mjTEXROLE_RGB),
    std::make_pair("mjTEXROLE_OCCLUSION", ::mjtTextureRole::mjTEXROLE_OCCLUSION),
    std::make_pair("mjTEXROLE_ROUGHNESS", ::mjtTextureRole::mjTEXROLE_ROUGHNESS),
    std::make_pair("mjTEXROLE_METALLIC", ::mjtTextureRole::mjTEXROLE_METALLIC),
    std::make_pair("mjTEXROLE_NORMAL", ::mjtTextureRole::mjTEXROLE_NORMAL),
    std::make_pair("mjTEXROLE_OPACITY", ::mjtTextureRole::mjTEXROLE_OPACITY),
    std::make_pair("mjTEXROLE_EMISSIVE", ::mjtTextureRole::mjTEXROLE_EMISSIVE),
    std::make_pair("mjTEXROLE_RGBA", ::mjtTextureRole::mjTEXROLE_RGBA),
    std::make_pair("mjTEXROLE_ORM", ::mjtTextureRole::mjTEXROLE_ORM),
    std::make_pair("mjNTEXROLE", ::mjtTextureRole::mjNTEXROLE)};
};

struct mjtIntegrator {
  static constexpr char name[] = "mjtIntegrator";
  using type = ::mjtIntegrator;
  static constexpr auto values = std::array{
    std::make_pair("mjINT_EULER", ::mjtIntegrator::mjINT_EULER),
    std::make_pair("mjINT_RK4", ::mjtIntegrator::mjINT_RK4),
    std::make_pair("mjINT_IMPLICIT", ::mjtIntegrator::mjINT_IMPLICIT),
    std::make_pair("mjINT_IMPLICITFAST", ::mjtIntegrator::mjINT_IMPLICITFAST)};
};

struct mjtCone {
  static constexpr char name[] = "mjtCone";
  using type = ::mjtCone;
  static constexpr auto values = std::array{
    std::make_pair("mjCONE_PYRAMIDAL", ::mjtCone::mjCONE_PYRAMIDAL),
    std::make_pair("mjCONE_ELLIPTIC", ::mjtCone::mjCONE_ELLIPTIC)};
};

struct mjtJacobian {
  static constexpr char name[] = "mjtJacobian";
  using type = ::mjtJacobian;
  static constexpr auto values = std::array{
    std::make_pair("mjJAC_DENSE", ::mjtJacobian::mjJAC_DENSE),
    std::make_pair("mjJAC_SPARSE", ::mjtJacobian::mjJAC_SPARSE),
    std::make_pair("mjJAC_AUTO", ::mjtJacobian::mjJAC_AUTO)};
};

struct mjtSolver {
  static constexpr char name[] = "mjtSolver";
  using type = ::mjtSolver;
  static constexpr auto values = std::array{
    std::make_pair("mjSOL_PGS", ::mjtSolver::mjSOL_PGS),
    std::make_pair("mjSOL_CG", ::mjtSolver::mjSOL_CG),
    std::make_pair("mjSOL_NEWTON", ::mjtSolver::mjSOL_NEWTON)};
};

struct mjtEq {
  static constexpr char name[] = "mjtEq";
  using type = ::mjtEq;
  static constexpr auto values = std::array{
    std::make_pair("mjEQ_CONNECT", ::mjtEq::mjEQ_CONNECT),
    std::make_pair("mjEQ_WELD", ::mjtEq::mjEQ_WELD),
    std::make_pair("mjEQ_JOINT", ::mjtEq::mjEQ_JOINT),
    std::make_pair("mjEQ_TENDON", ::mjtEq::mjEQ_TENDON),
    std::make_pair("mjEQ_FLEX", ::mjtEq::mjEQ_FLEX),
    std::make_pair("mjEQ_DISTANCE", ::mjtEq::mjEQ_DISTANCE)};
};

struct mjtWrap {
  static constexpr char name[] = "mjtWrap";
  using type = ::mjtWrap;
  static constexpr auto values = std::array{
    std::make_pair("mjWRAP_NONE", ::mjtWrap::mjWRAP_NONE),
    std::make_pair("mjWRAP_JOINT", ::mjtWrap::mjWRAP_JOINT),
    std::make_pair("mjWRAP_PULLEY", ::mjtWrap::mjWRAP_PULLEY),
    std::make_pair("mjWRAP_SITE", ::mjtWrap::mjWRAP_SITE),
    std::make_pair("mjWRAP_SPHERE", ::mjtWrap::mjWRAP_SPHERE),
    std::make_pair("mjWRAP_CYLINDER", ::mjtWrap::mjWRAP_CYLINDER)};
};

struct mjtTrn {
  static constexpr char name[] = "mjtTrn";
  using type = ::mjtTrn;
  static constexpr auto values = std::array{
    std::make_pair("mjTRN_JOINT", ::mjtTrn::mjTRN_JOINT),
    std::make_pair("mjTRN_JOINTINPARENT", ::mjtTrn::mjTRN_JOINTINPARENT),
    std::make_pair("mjTRN_SLIDERCRANK", ::mjtTrn::mjTRN_SLIDERCRANK),
    std::make_pair("mjTRN_TENDON", ::mjtTrn::mjTRN_TENDON),
    std::make_pair("mjTRN_SITE", ::mjtTrn::mjTRN_SITE),
    std::make_pair("mjTRN_BODY", ::mjtTrn::mjTRN_BODY),
    std::make_pair("mjTRN_UNDEFINED", ::mjtTrn::mjTRN_UNDEFINED)};
};

struct mjtDyn {
  static constexpr char name[] = "mjtDyn";
  using type = ::mjtDyn;
  static constexpr auto values = std::array{
    std::make_pair("mjDYN_NONE", ::mjtDyn::mjDYN_NONE),
    std::make_pair("mjDYN_INTEGRATOR", ::mjtDyn::mjDYN_INTEGRATOR),
    std::make_pair("mjDYN_FILTER", ::mjtDyn::mjDYN_FILTER),
    std::make_pair("mjDYN_FILTEREXACT", ::mjtDyn::mjDYN_FILTEREXACT),
    std::make_pair("mjDYN_MUSCLE", ::mjtDyn::mjDYN_MUSCLE),
    std::make_pair("mjDYN_USER", ::mjtDyn::mjDYN_USER)};
};

struct mjtGain {
  static constexpr char name[] = "mjtGain";
  using type = ::mjtGain;
  static constexpr auto values = std::array{
    std::make_pair("mjGAIN_FIXED", ::mjtGain::mjGAIN_FIXED),
    std::make_pair("mjGAIN_AFFINE", ::mjtGain::mjGAIN_AFFINE),
    std::make_pair("mjGAIN_MUSCLE", ::mjtGain::mjGAIN_MUSCLE),
    std::make_pair("mjGAIN_USER", ::mjtGain::mjGAIN_USER)};
};

struct mjtBias {
  static constexpr char name[] = "mjtBias";
  using type = ::mjtBias;
  static constexpr auto values = std::array{
    std::make_pair("mjBIAS_NONE", ::mjtBias::mjBIAS_NONE),
    std::make_pair("mjBIAS_AFFINE", ::mjtBias::mjBIAS_AFFINE),
    std::make_pair("mjBIAS_MUSCLE", ::mjtBias::mjBIAS_MUSCLE),
    std::make_pair("mjBIAS_USER", ::mjtBias::mjBIAS_USER)};
};

struct mjtObj {
  static constexpr char name[] = "mjtObj";
  using type = ::mjtObj;
  static constexpr auto values = std::array{
    std::make_pair("mjOBJ_UNKNOWN", ::mjtObj::mjOBJ_UNKNOWN),
    std::make_pair("mjOBJ_BODY", ::mjtObj::mjOBJ_BODY),
    std::make_pair("mjOBJ_XBODY", ::mjtObj::mjOBJ_XBODY),
    std::make_pair("mjOBJ_JOINT", ::mjtObj::mjOBJ_JOINT),
    std::make_pair("mjOBJ_DOF", ::mjtObj::mjOBJ_DOF),
    std::make_pair("mjOBJ_GEOM", ::mjtObj::mjOBJ_GEOM),
    std::make_pair("mjOBJ_SITE", ::mjtObj::mjOBJ_SITE),
    std::make_pair("mjOBJ_CAMERA", ::mjtObj::mjOBJ_CAMERA),
    std::make_pair("mjOBJ_LIGHT", ::mjtObj::mjOBJ_LIGHT),
    std::make_pair("mjOBJ_FLEX", ::mjtObj::mjOBJ_FLEX),
    std::make_pair("mjOBJ_MESH", ::mjtObj::mjOBJ_MESH),
    std::make_pair("mjOBJ_SKIN", ::mjtObj::mjOBJ_SKIN),
    std::make_pair("mjOBJ_HFIELD", ::mjtObj::mjOBJ_HFIELD),
    std::make_pair("mjOBJ_TEXTURE", ::mjtObj::mjOBJ_TEXTURE),
    std::make_pair("mjOBJ_MATERIAL", ::mjtObj::mjOBJ_MATERIAL),
    std::make_pair("mjOBJ_PAIR", ::mjtObj::mjOBJ_PAIR),
    std::make_pair("mjOBJ_EXCLUDE", ::mjtObj::mjOBJ_EXCLUDE),
    std::make_pair("mjOBJ_EQUALITY", ::mjtObj::mjOBJ_EQUALITY),
    std::make_pair("mjOBJ_TENDON", ::mjtObj::mjOBJ_TENDON),
    std::make_pair("mjOBJ_ACTUATOR", ::mjtObj::mjOBJ_ACTUATOR),
    std::make_pair("mjOBJ_SENSOR", ::mjtObj::mjOBJ_SENSOR),
    std::make_pair("mjOBJ_NUMERIC", ::mjtObj::mjOBJ_NUMERIC),
    std::make_pair("mjOBJ_TEXT", ::mjtObj::mjOBJ_TEXT),
    std::make_pair("mjOBJ_TUPLE", ::mjtObj::mjOBJ_TUPLE),
    std::make_pair("mjOBJ_KEY", ::mjtObj::mjOBJ_KEY),
    std::make_pair("mjOBJ_PLUGIN", ::mjtObj::mjOBJ_PLUGIN),
    std::make_pair("mjNOBJECT", ::mjtObj::mjNOBJECT),
    std::make_pair("mjOBJ_FRAME", ::mjtObj::mjOBJ_FRAME),
    std::make_pair("mjOBJ_DEFAULT", ::mjtObj::mjOBJ_DEFAULT),
    std::make_pair("mjOBJ_MODEL", ::mjtObj::mjOBJ_MODEL)};
};

struct mjtConstraint {
  static constexpr char name[] = "mjtConstraint";
  using type = ::mjtConstraint;
  static constexpr auto values = std::array{
    std::make_pair("mjCNSTR_EQUALITY", ::mjtConstraint::mjCNSTR_EQUALITY),
    std::make_pair("mjCNSTR_FRICTION_DOF", ::mjtConstraint::mjCNSTR_FRICTION_DOF),
    std::make_pair("mjCNSTR_FRICTION_TENDON", ::mjtConstraint::mjCNSTR_FRICTION_TENDON),
    std::make_pair("mjCNSTR_LIMIT_JOINT", ::mjtConstraint::mjCNSTR_LIMIT_JOINT),
    std::make_pair("mjCNSTR_LIMIT_TENDON", ::mjtConstraint::mjCNSTR_LIMIT_TENDON),
    std::make_pair("mjCNSTR_CONTACT_FRICTIONLESS", ::mjtConstraint::mjCNSTR_CONTACT_FRICTIONLESS),
    std::make_pair("mjCNSTR_CONTACT_PYRAMIDAL", ::mjtConstraint::mjCNSTR_CONTACT_PYRAMIDAL),
    std::make_pair("mjCNSTR_CONTACT_ELLIPTIC", ::mjtConstraint::mjCNSTR_CONTACT_ELLIPTIC)};
};

struct mjtConstraintState {
  static constexpr char name[] = "mjtConstraintState";
  using type = ::mjtConstraintState;
  static constexpr auto values = std::array{
    std::make_pair("mjCNSTRSTATE_SATISFIED", ::mjtConstraintState::mjCNSTRSTATE_SATISFIED),
    std::make_pair("mjCNSTRSTATE_QUADRATIC", ::mjtConstraintState::mjCNSTRSTATE_QUADRATIC),
    std::make_pair("mjCNSTRSTATE_LINEARNEG", ::mjtConstraintState::mjCNSTRSTATE_LINEARNEG),
    std::make_pair("mjCNSTRSTATE_LINEARPOS", ::mjtConstraintState::mjCNSTRSTATE_LINEARPOS),
    std::make_pair("mjCNSTRSTATE_CONE", ::mjtConstraintState::mjCNSTRSTATE_CONE)};
};

struct mjtSensor {
  static constexpr char name[] = "mjtSensor";
  using type = ::mjtSensor;
  static constexpr auto values = std::array{
    std::make_pair("mjSENS_TOUCH", ::mjtSensor::mjSENS_TOUCH),
    std::make_pair("mjSENS_ACCELEROMETER", ::mjtSensor::mjSENS_ACCELEROMETER),
    std::make_pair("mjSENS_VELOCIMETER", ::mjtSensor::mjSENS_VELOCIMETER),
    std::make_pair("mjSENS_GYRO", ::mjtSensor::mjSENS_GYRO),
    std::make_pair("mjSENS_FORCE", ::mjtSensor::mjSENS_FORCE),
    std::make_pair("mjSENS_TORQUE", ::mjtSensor::mjSENS_TORQUE),
    std::make_pair("mjSENS_MAGNETOMETER", ::mjtSensor::mjSENS_MAGNETOMETER),
    std::make_pair("mjSENS_RANGEFINDER", ::mjtSensor::mjSENS_RANGEFINDER),
    std::make_pair("mjSENS_CAMPROJECTION", ::mjtSensor::mjSENS_CAMPROJECTION),
    std::make_pair("mjSENS_JOINTPOS", ::mjtSensor::mjSENS_JOINTPOS),
    std::make_pair("mjSENS_JOINTVEL", ::mjtSensor::mjSENS_JOINTVEL),
    std::make_pair("mjSENS_TENDONPOS", ::mjtSensor::mjSENS_TENDONPOS),
    std::make_pair("mjSENS_TENDONVEL", ::mjtSensor::mjSENS_TENDONVEL),
    std::make_pair("mjSENS_ACTUATORPOS", ::mjtSensor::mjSENS_ACTUATORPOS),
    std::make_pair("mjSENS_ACTUATORVEL", ::mjtSensor::mjSENS_ACTUATORVEL),
    std::make_pair("mjSENS_ACTUATORFRC", ::mjtSensor::mjSENS_ACTUATORFRC),
    std::make_pair("mjSENS_JOINTACTFRC", ::mjtSensor::mjSENS_JOINTACTFRC),
    std::make_pair("mjSENS_TENDONACTFRC", ::mjtSensor::mjSENS_TENDONACTFRC),
    std::make_pair("mjSENS_BALLQUAT", ::mjtSensor::mjSENS_BALLQUAT),
    std::make_pair("mjSENS_BALLANGVEL", ::mjtSensor::mjSENS_BALLANGVEL),
    std::make_pair("mjSENS_JOINTLIMITPOS", ::mjtSensor::mjSENS_JOINTLIMITPOS),
    std::make_pair("mjSENS_JOINTLIMITVEL", ::mjtSensor::mjSENS_JOINTLIMITVEL),
    std::make_pair("mjSENS_JOINTLIMITFRC", ::mjtSensor::mjSENS_JOINTLIMITFRC),
    std::make_pair("mjSENS_TENDONLIMITPOS", ::mjtSensor::mjSENS_TENDONLIMITPOS),
    std::make_pair("mjSENS_TENDONLIMITVEL", ::mjtSensor::mjSENS_TENDONLIMITVEL),
    std::make_pair("mjSENS_TENDONLIMITFRC", ::mjtSensor::mjSENS_TENDONLIMITFRC),
    std::make_pair("mjSENS_FRAMEPOS", ::mjtSensor::mjSENS_FRAMEPOS),
    std::make_pair("mjSENS_FRAMEQUAT", ::mjtSensor::mjSENS_FRAMEQUAT),
    std::make_pair("mjSENS_FRAMEXAXIS", ::mjtSensor::mjSENS_FRAMEXAXIS),
    std::make_pair("mjSENS_FRAMEYAXIS", ::mjtSensor::mjSENS_FRAMEYAXIS),
    std::make_pair("mjSENS_FRAMEZAXIS", ::mjtSensor::mjSENS_FRAMEZAXIS),
    std::make_pair("mjSENS_FRAMELINVEL", ::mjtSensor::mjSENS_FRAMELINVEL),
    std::make_pair("mjSENS_FRAMEANGVEL", ::mjtSensor::mjSENS_FRAMEANGVEL),
    std::make_pair("mjSENS_FRAMELINACC", ::mjtSensor::mjSENS_FRAMELINACC),
    std::make_pair("mjSENS_FRAMEANGACC", ::mjtSensor::mjSENS_FRAMEANGACC),
    std::make_pair("mjSENS_SUBTREECOM", ::mjtSensor::mjSENS_SUBTREECOM),
    std::make_pair("mjSENS_SUBTREELINVEL", ::mjtSensor::mjSENS_SUBTREELINVEL),
    std::make_pair("mjSENS_SUBTREEANGMOM", ::mjtSensor::mjSENS_SUBTREEANGMOM),
    std::make_pair("mjSENS_GEOMDIST", ::mjtSensor::mjSENS_GEOMDIST),
    std::make_pair("mjSENS_GEOMNORMAL", ::mjtSensor::mjSENS_GEOMNORMAL),
    std::make_pair("mjSENS_GEOMFROMTO", ::mjtSensor::mjSENS_GEOMFROMTO),
    std::make_pair("mjSENS_E_POTENTIAL", ::mjtSensor::mjSENS_E_POTENTIAL),
    std::make_pair("mjSENS_E_KINETIC", ::mjtSensor::mjSENS_E_KINETIC),
    std::make_pair("mjSENS_CLOCK", ::mjtSensor::mjSENS_CLOCK),
    std::make_pair("mjSENS_PLUGIN", ::mjtSensor::mjSENS_PLUGIN),
    std::make_pair("mjSENS_USER", ::mjtSensor::mjSENS_USER)};
};

struct mjtStage {
  static constexpr char name[] = "mjtStage";
  using type = ::mjtStage;
  static constexpr auto values = std::array{
    std::make_pair("mjSTAGE_NONE", ::mjtStage::mjSTAGE_NONE),
    std::make_pair("mjSTAGE_POS", ::mjtStage::mjSTAGE_POS),
    std::make_pair("mjSTAGE_VEL", ::mjtStage::mjSTAGE_VEL),
    std::make_pair("mjSTAGE_ACC", ::mjtStage::mjSTAGE_ACC)};
};

struct mjtDataType {
  static constexpr char name[] = "mjtDataType";
  using type = ::mjtDataType;
  static constexpr auto values = std::array{
    std::make_pair("mjDATATYPE_REAL", ::mjtDataType::mjDATATYPE_REAL),
    std::make_pair("mjDATATYPE_POSITIVE", ::mjtDataType::mjDATATYPE_POSITIVE),
    std::make_pair("mjDATATYPE_AXIS", ::mjtDataType::mjDATATYPE_AXIS),
    std::make_pair("mjDATATYPE_QUATERNION", ::mjtDataType::mjDATATYPE_QUATERNION)};
};

struct mjtSameFrame {
  static constexpr char name[] = "mjtSameFrame";
  using type = ::mjtSameFrame;
  static constexpr auto values = std::array{
    std::make_pair("mjSAMEFRAME_NONE", ::mjtSameFrame::mjSAMEFRAME_NONE),
    std::make_pair("mjSAMEFRAME_BODY", ::mjtSameFrame::mjSAMEFRAME_BODY),
    std::make_pair("mjSAMEFRAME_INERTIA", ::mjtSameFrame::mjSAMEFRAME_INERTIA),
    std::make_pair("mjSAMEFRAME_BODYROT", ::mjtSameFrame::mjSAMEFRAME_BODYROT),
    std::make_pair("mjSAMEFRAME_INERTIAROT", ::mjtSameFrame::mjSAMEFRAME_INERTIAROT)};
};

struct mjtLRMode {
  static constexpr char name[] = "mjtLRMode";
  using type = ::mjtLRMode;
  static constexpr auto values = std::array{
    std::make_pair("mjLRMODE_NONE", ::mjtLRMode::mjLRMODE_NONE),
    std::make_pair("mjLRMODE_MUSCLE", ::mjtLRMode::mjLRMODE_MUSCLE),
    std::make_pair("mjLRMODE_MUSCLEUSER", ::mjtLRMode::mjLRMODE_MUSCLEUSER),
    std::make_pair("mjLRMODE_ALL", ::mjtLRMode::mjLRMODE_ALL)};
};

struct mjtFlexSelf {
  static constexpr char name[] = "mjtFlexSelf";
  using type = ::mjtFlexSelf;
  static constexpr auto values = std::array{
    std::make_pair("mjFLEXSELF_NONE", ::mjtFlexSelf::mjFLEXSELF_NONE),
    std::make_pair("mjFLEXSELF_NARROW", ::mjtFlexSelf::mjFLEXSELF_NARROW),
    std::make_pair("mjFLEXSELF_BVH", ::mjtFlexSelf::mjFLEXSELF_BVH),
    std::make_pair("mjFLEXSELF_SAP", ::mjtFlexSelf::mjFLEXSELF_SAP),
    std::make_pair("mjFLEXSELF_AUTO", ::mjtFlexSelf::mjFLEXSELF_AUTO)};
};

struct mjtTaskStatus {
  static constexpr char name[] = "mjtTaskStatus";
  using type = ::mjtTaskStatus;
  static constexpr auto values = std::array{
    std::make_pair("mjTASK_NEW", ::mjtTaskStatus::mjTASK_NEW),
    std::make_pair("mjTASK_QUEUED", ::mjtTaskStatus::mjTASK_QUEUED),
    std::make_pair("mjTASK_COMPLETED", ::mjtTaskStatus::mjTASK_COMPLETED)};
};

struct mjtState {
  static constexpr char name[] = "mjtState";
  using type = ::mjtState;
  static constexpr auto values = std::array{
    std::make_pair("mjSTATE_TIME", ::mjtState::mjSTATE_TIME),
    std::make_pair("mjSTATE_QPOS", ::mjtState::mjSTATE_QPOS),
    std::make_pair("mjSTATE_QVEL", ::mjtState::mjSTATE_QVEL),
    std::make_pair("mjSTATE_ACT", ::mjtState::mjSTATE_ACT),
    std::make_pair("mjSTATE_WARMSTART", ::mjtState::mjSTATE_WARMSTART),
    std::make_pair("mjSTATE_CTRL", ::mjtState::mjSTATE_CTRL),
    std::make_pair("mjSTATE_QFRC_APPLIED", ::mjtState::mjSTATE_QFRC_APPLIED),
    std::make_pair("mjSTATE_XFRC_APPLIED", ::mjtState::mjSTATE_XFRC_APPLIED),
    std::make_pair("mjSTATE_EQ_ACTIVE", ::mjtState::mjSTATE_EQ_ACTIVE),
    std::make_pair("mjSTATE_MOCAP_POS", ::mjtState::mjSTATE_MOCAP_POS),
    std::make_pair("mjSTATE_MOCAP_QUAT", ::mjtState::mjSTATE_MOCAP_QUAT),
    std::make_pair("mjSTATE_USERDATA", ::mjtState::mjSTATE_USERDATA),
    std::make_pair("mjSTATE_PLUGIN", ::mjtState::mjSTATE_PLUGIN),
    std::make_pair("mjNSTATE", ::mjtState::mjNSTATE),
    std::make_pair("mjSTATE_PHYSICS", ::mjtState::mjSTATE_PHYSICS),
    std::make_pair("mjSTATE_FULLPHYSICS", ::mjtState::mjSTATE_FULLPHYSICS),
    std::make_pair("mjSTATE_USER", ::mjtState::mjSTATE_USER),
    std::make_pair("mjSTATE_INTEGRATION", ::mjtState::mjSTATE_INTEGRATION)};
};

struct mjtWarning {
  static constexpr char name[] = "mjtWarning";
  using type = ::mjtWarning;
  static constexpr auto values = std::array{
    std::make_pair("mjWARN_INERTIA", ::mjtWarning::mjWARN_INERTIA),
    std::make_pair("mjWARN_CONTACTFULL", ::mjtWarning::mjWARN_CONTACTFULL),
    std::make_pair("mjWARN_CNSTRFULL", ::mjtWarning::mjWARN_CNSTRFULL),
    std::make_pair("mjWARN_VGEOMFULL", ::mjtWarning::mjWARN_VGEOMFULL),
    std::make_pair("mjWARN_BADQPOS", ::mjtWarning::mjWARN_BADQPOS),
    std::make_pair("mjWARN_BADQVEL", ::mjtWarning::mjWARN_BADQVEL),
    std::make_pair("mjWARN_BADQACC", ::mjtWarning::mjWARN_BADQACC),
    std::make_pair("mjWARN_BADCTRL", ::mjtWarning::mjWARN_BADCTRL),
    std::make_pair("mjNWARNING", ::mjtWarning::mjNWARNING)};
};

struct mjtTimer {
  static constexpr char name[] = "mjtTimer";
  using type = ::mjtTimer;
  static constexpr auto values = std::array{
    std::make_pair("mjTIMER_STEP", ::mjtTimer::mjTIMER_STEP),
    std::make_pair("mjTIMER_FORWARD", ::mjtTimer::mjTIMER_FORWARD),
    std::make_pair("mjTIMER_INVERSE", ::mjtTimer::mjTIMER_INVERSE),
    std::make_pair("mjTIMER_POSITION", ::mjtTimer::mjTIMER_POSITION),
    std::make_pair("mjTIMER_VELOCITY", ::mjtTimer::mjTIMER_VELOCITY),
    std::make_pair("mjTIMER_ACTUATION", ::mjtTimer::mjTIMER_ACTUATION),
    std::make_pair("mjTIMER_CONSTRAINT", ::mjtTimer::mjTIMER_CONSTRAINT),
    std::make_pair("mjTIMER_ADVANCE", ::mjtTimer::mjTIMER_ADVANCE),
    std::make_pair("mjTIMER_POS_KINEMATICS", ::mjtTimer::mjTIMER_POS_KINEMATICS),
    std::make_pair("mjTIMER_POS_INERTIA", ::mjtTimer::mjTIMER_POS_INERTIA),
    std::make_pair("mjTIMER_POS_COLLISION", ::mjtTimer::mjTIMER_POS_COLLISION),
    std::make_pair("mjTIMER_POS_MAKE", ::mjtTimer::mjTIMER_POS_MAKE),
    std::make_pair("mjTIMER_POS_PROJECT", ::mjtTimer::mjTIMER_POS_PROJECT),
    std::make_pair("mjTIMER_COL_BROAD", ::mjtTimer::mjTIMER_COL_BROAD),
    std::make_pair("mjTIMER_COL_NARROW", ::mjtTimer::mjTIMER_COL_NARROW),
    std::make_pair("mjNTIMER", ::mjtTimer::mjNTIMER)};
};

struct mjtCatBit {
  static constexpr char name[] = "mjtCatBit";
  using type = ::mjtCatBit;
  static constexpr auto values = std::array{
    std::make_pair("mjCAT_STATIC", ::mjtCatBit::mjCAT_STATIC),
    std::make_pair("mjCAT_DYNAMIC", ::mjtCatBit::mjCAT_DYNAMIC),
    std::make_pair("mjCAT_DECOR", ::mjtCatBit::mjCAT_DECOR),
    std::make_pair("mjCAT_ALL", ::mjtCatBit::mjCAT_ALL)};
};

struct mjtMouse {
  static constexpr char name[] = "mjtMouse";
  using type = ::mjtMouse;
  static constexpr auto values = std::array{
    std::make_pair("mjMOUSE_NONE", ::mjtMouse::mjMOUSE_NONE),
    std::make_pair("mjMOUSE_ROTATE_V", ::mjtMouse::mjMOUSE_ROTATE_V),
    std::make_pair("mjMOUSE_ROTATE_H", ::mjtMouse::mjMOUSE_ROTATE_H),
    std::make_pair("mjMOUSE_MOVE_V", ::mjtMouse::mjMOUSE_MOVE_V),
    std::make_pair("mjMOUSE_MOVE_H", ::mjtMouse::mjMOUSE_MOVE_H),
    std::make_pair("mjMOUSE_ZOOM", ::mjtMouse::mjMOUSE_ZOOM),
    std::make_pair("mjMOUSE_SELECT", ::mjtMouse::mjMOUSE_SELECT)};
};

struct mjtPertBit {
  static constexpr char name[] = "mjtPertBit";
  using type = ::mjtPertBit;
  static constexpr auto values = std::array{
    std::make_pair("mjPERT_TRANSLATE", ::mjtPertBit::mjPERT_TRANSLATE),
    std::make_pair("mjPERT_ROTATE", ::mjtPertBit::mjPERT_ROTATE)};
};

struct mjtCamera {
  static constexpr char name[] = "mjtCamera";
  using type = ::mjtCamera;
  static constexpr auto values = std::array{
    std::make_pair("mjCAMERA_FREE", ::mjtCamera::mjCAMERA_FREE),
    std::make_pair("mjCAMERA_TRACKING", ::mjtCamera::mjCAMERA_TRACKING),
    std::make_pair("mjCAMERA_FIXED", ::mjtCamera::mjCAMERA_FIXED),
    std::make_pair("mjCAMERA_USER", ::mjtCamera::mjCAMERA_USER)};
};

struct mjtLabel {
  static constexpr char name[] = "mjtLabel";
  using type = ::mjtLabel;
  static constexpr auto values = std::array{
    std::make_pair("mjLABEL_NONE", ::mjtLabel::mjLABEL_NONE),
    std::make_pair("mjLABEL_BODY", ::mjtLabel::mjLABEL_BODY),
    std::make_pair("mjLABEL_JOINT", ::mjtLabel::mjLABEL_JOINT),
    std::make_pair("mjLABEL_GEOM", ::mjtLabel::mjLABEL_GEOM),
    std::make_pair("mjLABEL_SITE", ::mjtLabel::mjLABEL_SITE),
    std::make_pair("mjLABEL_CAMERA", ::mjtLabel::mjLABEL_CAMERA),
    std::make_pair("mjLABEL_LIGHT", ::mjtLabel::mjLABEL_LIGHT),
    std::make_pair("mjLABEL_TENDON", ::mjtLabel::mjLABEL_TENDON),
    std::make_pair("mjLABEL_ACTUATOR", ::mjtLabel::mjLABEL_ACTUATOR),
    std::make_pair("mjLABEL_CONSTRAINT", ::mjtLabel::mjLABEL_CONSTRAINT),
    std::make_pair("mjLABEL_FLEX", ::mjtLabel::mjLABEL_FLEX),
    std::make_pair("mjLABEL_SKIN", ::mjtLabel::mjLABEL_SKIN),
    std::make_pair("mjLABEL_SELECTION", ::mjtLabel::mjLABEL_SELECTION),
    std::make_pair("mjLABEL_SELPNT", ::mjtLabel::mjLABEL_SELPNT),
    std::make_pair("mjLABEL_CONTACTPOINT", ::mjtLabel::mjLABEL_CONTACTPOINT),
    std::make_pair("mjLABEL_CONTACTFORCE", ::mjtLabel::mjLABEL_CONTACTFORCE),
    std::make_pair("mjLABEL_ISLAND", ::mjtLabel::mjLABEL_ISLAND),
    std::make_pair("mjNLABEL", ::mjtLabel::mjNLABEL)};
};

struct mjtFrame {
  static constexpr char name[] = "mjtFrame";
  using type = ::mjtFrame;
  static constexpr auto values = std::array{
    std::make_pair("mjFRAME_NONE", ::mjtFrame::mjFRAME_NONE),
    std::make_pair("mjFRAME_BODY", ::mjtFrame::mjFRAME_BODY),
    std::make_pair("mjFRAME_GEOM", ::mjtFrame::mjFRAME_GEOM),
    std::make_pair("mjFRAME_SITE", ::mjtFrame::mjFRAME_SITE),
    std::make_pair("mjFRAME_CAMERA", ::mjtFrame::mjFRAME_CAMERA),
    std::make_pair("mjFRAME_LIGHT", ::mjtFrame::mjFRAME_LIGHT),
    std::make_pair("mjFRAME_CONTACT", ::mjtFrame::mjFRAME_CONTACT),
    std::make_pair("mjFRAME_WORLD", ::mjtFrame::mjFRAME_WORLD),
    std::make_pair("mjNFRAME", ::mjtFrame::mjNFRAME)};
};

struct mjtVisFlag {
  static constexpr char name[] = "mjtVisFlag";
  using type = ::mjtVisFlag;
  static constexpr auto values = std::array{
    std::make_pair("mjVIS_CONVEXHULL", ::mjtVisFlag::mjVIS_CONVEXHULL),
    std::make_pair("mjVIS_TEXTURE", ::mjtVisFlag::mjVIS_TEXTURE),
    std::make_pair("mjVIS_JOINT", ::mjtVisFlag::mjVIS_JOINT),
    std::make_pair("mjVIS_CAMERA", ::mjtVisFlag::mjVIS_CAMERA),
    std::make_pair("mjVIS_ACTUATOR", ::mjtVisFlag::mjVIS_ACTUATOR),
    std::make_pair("mjVIS_ACTIVATION", ::mjtVisFlag::mjVIS_ACTIVATION),
    std::make_pair("mjVIS_LIGHT", ::mjtVisFlag::mjVIS_LIGHT),
    std::make_pair("mjVIS_TENDON", ::mjtVisFlag::mjVIS_TENDON),
    std::make_pair("mjVIS_RANGEFINDER", ::mjtVisFlag::mjVIS_RANGEFINDER),
    std::make_pair("mjVIS_CONSTRAINT", ::mjtVisFlag::mjVIS_CONSTRAINT),
    std::make_pair("mjVIS_INERTIA", ::mjtVisFlag::mjVIS_INERTIA),
    std::make_pair("mjVIS_SCLINERTIA", ::mjtVisFlag::mjVIS_SCLINERTIA),
    std::make_pair("mjVIS_PERTFORCE", ::mjtVisFlag::mjVIS_PERTFORCE),
    std::make_pair("mjVIS_PERTOBJ", ::mjtVisFlag::mjVIS_PERTOBJ),
    std::make_pair("mjVIS_CONTACTPOINT", ::mjtVisFlag::mjVIS_CONTACTPOINT),
    std::make_pair("mjVIS_ISLAND", ::mjtVisFlag::mjVIS_ISLAND),
    std::make_pair("mjVIS_CONTACTFORCE", ::mjtVisFlag::mjVIS_CONTACTFORCE),
    std::make_pair("mjVIS_CONTACTSPLIT", ::mjtVisFlag::mjVIS_CONTACTSPLIT),
    std::make_pair("mjVIS_TRANSPARENT", ::mjtVisFlag::mjVIS_TRANSPARENT),
    std::make_pair("mjVIS_AUTOCONNECT", ::mjtVisFlag::mjVIS_AUTOCONNECT),
    std::make_pair("mjVIS_COM", ::mjtVisFlag::mjVIS_COM),
    std::make_pair("mjVIS_SELECT", ::mjtVisFlag::mjVIS_SELECT),
    std::make_pair("mjVIS_STATIC", ::mjtVisFlag::mjVIS_STATIC),
    std::make_pair("mjVIS_SKIN", ::mjtVisFlag::mjVIS_SKIN),
    std::make_pair("mjVIS_FLEXVERT", ::mjtVisFlag::mjVIS_FLEXVERT),
    std::make_pair("mjVIS_FLEXEDGE", ::mjtVisFlag::mjVIS_FLEXEDGE),
    std::make_pair("mjVIS_FLEXFACE", ::mjtVisFlag::mjVIS_FLEXFACE),
    std::make_pair("mjVIS_FLEXSKIN", ::mjtVisFlag::mjVIS_FLEXSKIN),
    std::make_pair("mjVIS_BODYBVH", ::mjtVisFlag::mjVIS_BODYBVH),
    std::make_pair("mjVIS_FLEXBVH", ::mjtVisFlag::mjVIS_FLEXBVH),
    std::make_pair("mjVIS_MESHBVH", ::mjtVisFlag::mjVIS_MESHBVH),
    std::make_pair("mjVIS_SDFITER", ::mjtVisFlag::mjVIS_SDFITER),
    std::make_pair("mjNVISFLAG", ::mjtVisFlag::mjNVISFLAG)};
};

struct mjtRndFlag {
  static constexpr char name[] = "mjtRndFlag";
  using type = ::mjtRndFlag;
  static constexpr auto values = std::array{
    std::make_pair("mjRND_SHADOW", ::mjtRndFlag::mjRND_SHADOW),
    std::make_pair("mjRND_WIREFRAME", ::mjtRndFlag::mjRND_WIREFRAME),
    std::make_pair("mjRND_REFLECTION", ::mjtRndFlag::mjRND_REFLECTION),
    std::make_pair("mjRND_ADDITIVE", ::mjtRndFlag::mjRND_ADDITIVE),
    std::make_pair("mjRND_SKYBOX", ::mjtRndFlag::mjRND_SKYBOX),
    std::make_pair("mjRND_FOG", ::mjtRndFlag::mjRND_FOG),
    std::make_pair("mjRND_HAZE", ::mjtRndFlag::mjRND_HAZE),
    std::make_pair("mjRND_SEGMENT", ::mjtRndFlag::mjRND_SEGMENT),
    std::make_pair("mjRND_IDCOLOR", ::mjtRndFlag::mjRND_IDCOLOR),
    std::make_pair("mjRND_CULL_FACE", ::mjtRndFlag::mjRND_CULL_FACE),
    std::make_pair("mjNRNDFLAG", ::mjtRndFlag::mjNRNDFLAG)};
};

struct mjtStereo {
  static constexpr char name[] = "mjtStereo";
  using type = ::mjtStereo;
  static constexpr auto values = std::array{
    std::make_pair("mjSTEREO_NONE", ::mjtStereo::mjSTEREO_NONE),
    std::make_pair("mjSTEREO_QUADBUFFERED", ::mjtStereo::mjSTEREO_QUADBUFFERED),
    std::make_pair("mjSTEREO_SIDEBYSIDE", ::mjtStereo::mjSTEREO_SIDEBYSIDE)};
};

struct mjtPluginCapabilityBit {
  static constexpr char name[] = "mjtPluginCapabilityBit";
  using type = ::mjtPluginCapabilityBit;
  static constexpr auto values = std::array{
    std::make_pair("mjPLUGIN_ACTUATOR", ::mjtPluginCapabilityBit::mjPLUGIN_ACTUATOR),
    std::make_pair("mjPLUGIN_SENSOR", ::mjtPluginCapabilityBit::mjPLUGIN_SENSOR),
    std::make_pair("mjPLUGIN_PASSIVE", ::mjtPluginCapabilityBit::mjPLUGIN_PASSIVE),
    std::make_pair("mjPLUGIN_SDF", ::mjtPluginCapabilityBit::mjPLUGIN_SDF)};
};

struct mjtGridPos {
  static constexpr char name[] = "mjtGridPos";
  using type = ::mjtGridPos;
  static constexpr auto values = std::array{
    std::make_pair("mjGRID_TOPLEFT", ::mjtGridPos::mjGRID_TOPLEFT),
    std::make_pair("mjGRID_TOPRIGHT", ::mjtGridPos::mjGRID_TOPRIGHT),
    std::make_pair("mjGRID_BOTTOMLEFT", ::mjtGridPos::mjGRID_BOTTOMLEFT),
    std::make_pair("mjGRID_BOTTOMRIGHT", ::mjtGridPos::mjGRID_BOTTOMRIGHT),
    std::make_pair("mjGRID_TOP", ::mjtGridPos::mjGRID_TOP),
    std::make_pair("mjGRID_BOTTOM", ::mjtGridPos::mjGRID_BOTTOM),
    std::make_pair("mjGRID_LEFT", ::mjtGridPos::mjGRID_LEFT),
    std::make_pair("mjGRID_RIGHT", ::mjtGridPos::mjGRID_RIGHT)};
};

struct mjtFramebuffer {
  static constexpr char name[] = "mjtFramebuffer";
  using type = ::mjtFramebuffer;
  static constexpr auto values = std::array{
    std::make_pair("mjFB_WINDOW", ::mjtFramebuffer::mjFB_WINDOW),
    std::make_pair("mjFB_OFFSCREEN", ::mjtFramebuffer::mjFB_OFFSCREEN)};
};

struct mjtDepthMap {
  static constexpr char name[] = "mjtDepthMap";
  using type = ::mjtDepthMap;
  static constexpr auto values = std::array{
    std::make_pair("mjDEPTH_ZERONEAR", ::mjtDepthMap::mjDEPTH_ZERONEAR),
    std::make_pair("mjDEPTH_ZEROFAR", ::mjtDepthMap::mjDEPTH_ZEROFAR)};
};

struct mjtFontScale {
  static constexpr char name[] = "mjtFontScale";
  using type = ::mjtFontScale;
  static constexpr auto values = std::array{
    std::make_pair("mjFONTSCALE_50", ::mjtFontScale::mjFONTSCALE_50),
    std::make_pair("mjFONTSCALE_100", ::mjtFontScale::mjFONTSCALE_100),
    std::make_pair("mjFONTSCALE_150", ::mjtFontScale::mjFONTSCALE_150),
    std::make_pair("mjFONTSCALE_200", ::mjtFontScale::mjFONTSCALE_200),
    std::make_pair("mjFONTSCALE_250", ::mjtFontScale::mjFONTSCALE_250),
    std::make_pair("mjFONTSCALE_300", ::mjtFontScale::mjFONTSCALE_300)};
};

struct mjtFont {
  static constexpr char name[] = "mjtFont";
  using type = ::mjtFont;
  static constexpr auto values = std::array{
    std::make_pair("mjFONT_NORMAL", ::mjtFont::mjFONT_NORMAL),
    std::make_pair("mjFONT_SHADOW", ::mjtFont::mjFONT_SHADOW),
    std::make_pair("mjFONT_BIG", ::mjtFont::mjFONT_BIG)};
};

struct mjtGeomInertia {
  static constexpr char name[] = "mjtGeomInertia";
  using type = ::mjtGeomInertia;
  static constexpr auto values = std::array{
    std::make_pair("mjINERTIA_VOLUME", ::mjtGeomInertia::mjINERTIA_VOLUME),
    std::make_pair("mjINERTIA_SHELL", ::mjtGeomInertia::mjINERTIA_SHELL)};
};

struct mjtMeshInertia {
  static constexpr char name[] = "mjtMeshInertia";
  using type = ::mjtMeshInertia;
  static constexpr auto values = std::array{
    std::make_pair("mjMESH_INERTIA_CONVEX", ::mjtMeshInertia::mjMESH_INERTIA_CONVEX),
    std::make_pair("mjMESH_INERTIA_EXACT", ::mjtMeshInertia::mjMESH_INERTIA_EXACT),
    std::make_pair("mjMESH_INERTIA_LEGACY", ::mjtMeshInertia::mjMESH_INERTIA_LEGACY),
    std::make_pair("mjMESH_INERTIA_SHELL", ::mjtMeshInertia::mjMESH_INERTIA_SHELL)};
};

struct mjtBuiltin {
  static constexpr char name[] = "mjtBuiltin";
  using type = ::mjtBuiltin;
  static constexpr auto values = std::array{
    std::make_pair("mjBUILTIN_NONE", ::mjtBuiltin::mjBUILTIN_NONE),
    std::make_pair("mjBUILTIN_GRADIENT", ::mjtBuiltin::mjBUILTIN_GRADIENT),
    std::make_pair("mjBUILTIN_CHECKER", ::mjtBuiltin::mjBUILTIN_CHECKER),
    std::make_pair("mjBUILTIN_FLAT", ::mjtBuiltin::mjBUILTIN_FLAT)};
};

struct mjtMark {
  static constexpr char name[] = "mjtMark";
  using type = ::mjtMark;
  static constexpr auto values = std::array{
    std::make_pair("mjMARK_NONE", ::mjtMark::mjMARK_NONE),
    std::make_pair("mjMARK_EDGE", ::mjtMark::mjMARK_EDGE),
    std::make_pair("mjMARK_CROSS", ::mjtMark::mjMARK_CROSS),
    std::make_pair("mjMARK_RANDOM", ::mjtMark::mjMARK_RANDOM)};
};

struct mjtLimited {
  static constexpr char name[] = "mjtLimited";
  using type = ::mjtLimited;
  static constexpr auto values = std::array{
    std::make_pair("mjLIMITED_FALSE", ::mjtLimited::mjLIMITED_FALSE),
    std::make_pair("mjLIMITED_TRUE", ::mjtLimited::mjLIMITED_TRUE),
    std::make_pair("mjLIMITED_AUTO", ::mjtLimited::mjLIMITED_AUTO)};
};

struct mjtAlignFree {
  static constexpr char name[] = "mjtAlignFree";
  using type = ::mjtAlignFree;
  static constexpr auto values = std::array{
    std::make_pair("mjALIGNFREE_FALSE", ::mjtAlignFree::mjALIGNFREE_FALSE),
    std::make_pair("mjALIGNFREE_TRUE", ::mjtAlignFree::mjALIGNFREE_TRUE),
    std::make_pair("mjALIGNFREE_AUTO", ::mjtAlignFree::mjALIGNFREE_AUTO)};
};

struct mjtInertiaFromGeom {
  static constexpr char name[] = "mjtInertiaFromGeom";
  using type = ::mjtInertiaFromGeom;
  static constexpr auto values = std::array{
    std::make_pair("mjINERTIAFROMGEOM_FALSE", ::mjtInertiaFromGeom::mjINERTIAFROMGEOM_FALSE),
    std::make_pair("mjINERTIAFROMGEOM_TRUE", ::mjtInertiaFromGeom::mjINERTIAFROMGEOM_TRUE),
    std::make_pair("mjINERTIAFROMGEOM_AUTO", ::mjtInertiaFromGeom::mjINERTIAFROMGEOM_AUTO)};
};

struct mjtOrientation {
  static constexpr char name[] = "mjtOrientation";
  using type = ::mjtOrientation;
  static constexpr auto values = std::array{
    std::make_pair("mjORIENTATION_QUAT", ::mjtOrientation::mjORIENTATION_QUAT),
    std::make_pair("mjORIENTATION_AXISANGLE", ::mjtOrientation::mjORIENTATION_AXISANGLE),
    std::make_pair("mjORIENTATION_XYAXES", ::mjtOrientation::mjORIENTATION_XYAXES),
    std::make_pair("mjORIENTATION_ZAXIS", ::mjtOrientation::mjORIENTATION_ZAXIS),
    std::make_pair("mjORIENTATION_EULER", ::mjtOrientation::mjORIENTATION_EULER)};
};

struct mjtButton {
  static constexpr char name[] = "mjtButton";
  using type = ::mjtButton;
  static constexpr auto values = std::array{
    std::make_pair("mjBUTTON_NONE", ::mjtButton::mjBUTTON_NONE),
    std::make_pair("mjBUTTON_LEFT", ::mjtButton::mjBUTTON_LEFT),
    std::make_pair("mjBUTTON_RIGHT", ::mjtButton::mjBUTTON_RIGHT),
    std::make_pair("mjBUTTON_MIDDLE", ::mjtButton::mjBUTTON_MIDDLE)};
};

struct mjtEvent {
  static constexpr char name[] = "mjtEvent";
  using type = ::mjtEvent;
  static constexpr auto values = std::array{
    std::make_pair("mjEVENT_NONE", ::mjtEvent::mjEVENT_NONE),
    std::make_pair("mjEVENT_MOVE", ::mjtEvent::mjEVENT_MOVE),
    std::make_pair("mjEVENT_PRESS", ::mjtEvent::mjEVENT_PRESS),
    std::make_pair("mjEVENT_RELEASE", ::mjtEvent::mjEVENT_RELEASE),
    std::make_pair("mjEVENT_SCROLL", ::mjtEvent::mjEVENT_SCROLL),
    std::make_pair("mjEVENT_KEY", ::mjtEvent::mjEVENT_KEY),
    std::make_pair("mjEVENT_RESIZE", ::mjtEvent::mjEVENT_RESIZE),
    std::make_pair("mjEVENT_REDRAW", ::mjtEvent::mjEVENT_REDRAW),
    std::make_pair("mjEVENT_FILESDROP", ::mjtEvent::mjEVENT_FILESDROP)};
};

struct mjtItem {
  static constexpr char name[] = "mjtItem";
  using type = ::mjtItem;
  static constexpr auto values = std::array{
    std::make_pair("mjITEM_END", ::mjtItem::mjITEM_END),
    std::make_pair("mjITEM_SECTION", ::mjtItem::mjITEM_SECTION),
    std::make_pair("mjITEM_SEPARATOR", ::mjtItem::mjITEM_SEPARATOR),
    std::make_pair("mjITEM_STATIC", ::mjtItem::mjITEM_STATIC),
    std::make_pair("mjITEM_BUTTON", ::mjtItem::mjITEM_BUTTON),
    std::make_pair("mjITEM_CHECKINT", ::mjtItem::mjITEM_CHECKINT),
    std::make_pair("mjITEM_CHECKBYTE", ::mjtItem::mjITEM_CHECKBYTE),
    std::make_pair("mjITEM_RADIO", ::mjtItem::mjITEM_RADIO),
    std::make_pair("mjITEM_RADIOLINE", ::mjtItem::mjITEM_RADIOLINE),
    std::make_pair("mjITEM_SELECT", ::mjtItem::mjITEM_SELECT),
    std::make_pair("mjITEM_SLIDERINT", ::mjtItem::mjITEM_SLIDERINT),
    std::make_pair("mjITEM_SLIDERNUM", ::mjtItem::mjITEM_SLIDERNUM),
    std::make_pair("mjITEM_EDITINT", ::mjtItem::mjITEM_EDITINT),
    std::make_pair("mjITEM_EDITNUM", ::mjtItem::mjITEM_EDITNUM),
    std::make_pair("mjITEM_EDITFLOAT", ::mjtItem::mjITEM_EDITFLOAT),
    std::make_pair("mjITEM_EDITTXT", ::mjtItem::mjITEM_EDITTXT),
    std::make_pair("mjNITEM", ::mjtItem::mjNITEM)};
};

struct mjtSection {
  static constexpr char name[] = "mjtSection";
  using type = ::mjtSection;
  static constexpr auto values = std::array{
    std::make_pair("mjSECT_CLOSED", ::mjtSection::mjSECT_CLOSED),
    std::make_pair("mjSECT_OPEN", ::mjtSection::mjSECT_OPEN),
    std::make_pair("mjSECT_FIXED", ::mjtSection::mjSECT_FIXED)};
};

static constexpr auto kAllEnums = std::make_tuple(
    mjtDisableBit{},
    mjtEnableBit{},
    mjtJoint{},
    mjtGeom{},
    mjtCamLight{},
    mjtTexture{},
    mjtTextureRole{},
    mjtIntegrator{},
    mjtCone{},
    mjtJacobian{},
    mjtSolver{},
    mjtEq{},
    mjtWrap{},
    mjtTrn{},
    mjtDyn{},
    mjtGain{},
    mjtBias{},
    mjtObj{},
    mjtConstraint{},
    mjtConstraintState{},
    mjtSensor{},
    mjtStage{},
    mjtDataType{},
    mjtSameFrame{},
    mjtLRMode{},
    mjtFlexSelf{},
    mjtTaskStatus{},
    mjtState{},
    mjtWarning{},
    mjtTimer{},
    mjtCatBit{},
    mjtMouse{},
    mjtPertBit{},
    mjtCamera{},
    mjtLabel{},
    mjtFrame{},
    mjtVisFlag{},
    mjtRndFlag{},
    mjtStereo{},
    mjtPluginCapabilityBit{},
    mjtGridPos{},
    mjtFramebuffer{},
    mjtDepthMap{},
    mjtFontScale{},
    mjtFont{},
    mjtGeomInertia{},
    mjtMeshInertia{},
    mjtBuiltin{},
    mjtMark{},
    mjtLimited{},
    mjtAlignFree{},
    mjtInertiaFromGeom{},
    mjtOrientation{},
    mjtButton{},
    mjtEvent{},
    mjtItem{},
    mjtSection{});

}  // namespace mujoco::python_traits

#endif  // MUJOCO_PYTHON_CODEGEN_ENUM_TRAITS_H_

